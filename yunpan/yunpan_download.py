import os
import time
import math
import requests
import threading
from queue import Queue, Empty
from . import exceptions, base
from .conf import default_conf


class RemoteFile:
    def __init__(self, remote_path: str, session: requests.Session):
        self.session = session
        self.remote_path = remote_path
        self.url = "http://c.pcs.baidu.com/rest/2.0/pcs/file?method=download&app_id=250528&path={path}".format(
            path=remote_path)

        headers = default_conf.base_headers
        response = self.session.head(self.url, headers=default_conf.base_headers)
        if response.status_code == 404:
            raise exceptions.RemoteFileNotExistException(self.remote_path)
        response_headers = response.headers
        self.file_size = int(response_headers["x-bs-file-size"])
        self.etag = response_headers["Etag"]
        self.remote_md5 = response_headers["Content-MD5"]

        # math.ceil => 向上取整
        self.block_number = math.ceil(self.file_size / default_conf.download_block_size)
        # TODO 后期用于断点续传,暂时并没有意义
        self.to_download = [1, ] * self.block_number

    def download_to(self, target_path):
        target_dir = os.path.dirname(target_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        temp_file_path = ".".join((target_path, self.remote_md5, "fktd"))
        temp_file = open(temp_file_path, 'wb')
        # worker进程完成下载后将数据通过index_and_data_queue以(index,data)的形式发送至主线程
        # 特殊信息发送以(None,message)的形式发送到主线程
        self.index_and_data_queue = Queue()
        self.task_queue = Queue()
        for (index, i) in enumerate(self.to_download):
            if i != 0:
                self.task_queue.put(index)

        for i in range(default_conf.thread_pool_size):
            # 设置子线程为守护线程，主线程接收到足够多数据后直接退出
            t = threading.Thread(target=self.__download_worker, daemon=True)
            t.start()

        recved_block_number = 0
        # 当前存活的worker线程数量
        worker_number = default_conf.thread_pool_size
        while recved_block_number < self.block_number and worker_number > 0:
            try:
                (block_index, data) = self.index_and_data_queue.get_nowait()

                if block_index == None:
                    if isinstance(data, Exception):
                        worker_number -= 1
                        the_error = data
                        if isinstance(the_error, exceptions.RemoteFileHasBeenModified):
                            temp_file.close()
                            os.remove(temp_file_path)
                            raise the_error

                temp_file.seek(default_conf.download_block_size * block_index)
                temp_file.write(data)
                temp_file.flush()
                recved_block_number += 1
            except Empty:
                time.sleep(default_conf.poll_interval)

        temp_file.close()
        if os.path.exists(target_path):
            os.remove(target_path)
        os.rename(temp_file_path, target_path)

    def __download_worker(self):
        while True:
            block_index = self.task_queue.get()
            try:
                data = self.__download_one_block(block_index)
                self.index_and_data_queue.put((block_index, data))
            except exceptions.RemoteFileHasBeenModified as e:
                # 将异常信息发送到主线程，由主线程终止任务,子线程不抛出错误
                self.index_and_data_queue.put((None, e))
                return
            except Exception as e:
                # 将未完成的任务重新发布
                self.task_queue.put(block_index)
                # 将异常信息发送到主线程，主线程不抛出错误，子线程抛出错误帮助堆栈追踪
                self.index_and_data_queue.put((None, e))
                raise e

    def __download_one_block(self, block_index):
        start = block_index * default_conf.download_block_size
        end = (block_index + 1) * default_conf.download_block_size - 1
        # 坑爹BUG
        # 开始没有用base.user_agent_headers的copy方法
        # 瞎几把引用，浅拷贝然后下文Range的时候相互影响出错了
        headers = default_conf.base_headers
        headers["Range"] = "bytes={start}-{end}".format(start=start,
                                                        end=end)
        temp_response = self.session.get(url=self.url, headers=headers)
        if temp_response.headers["Etag"] != self.etag:
            raise exceptions.RemoteFileHasBeenModified

        if temp_response.status_code == 206:
            return temp_response.content
        else:
            base.process_remote_error_message(temp_response.text, self.remote_path)
