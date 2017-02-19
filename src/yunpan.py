import os
import threading
from queue import Queue, Empty

import base
import exceptions
import log_info
import requests

from src.conf import default_conf


class YunPan:
    def __init__(self,
                 user_name: str,
                 password: str,
                 cookie_path: str = default_conf.cookie_file_path,
                 auto_save: bool = False,
                 auto_load: bool = False):
        self.log_info = log_info.LogInfo(
            user_name=user_name,
            password=password,
            cookie_path=cookie_path,
            auto_load=auto_load,
            auto_save=auto_save
        )
        self.session = self.log_info.session

    def download_one_file(self, remote_path: str, local_path: str = None):
        self.log_info.check_login()
        if "/" not in remote_path:
            raise exceptions.RemoteFileNotExistException(remote_path)
        if remote_path.endswith("/"):
            raise exceptions.CanNotDownloadException
        if local_path is None:
            local_path = os.path.join(default_conf.target_dir, remote_path.split("/")[-1])

        the_remote_file = RemoteFile(remote_path, local_path, self.session)
        print(the_remote_file.url)
        the_remote_file.download()


class RemoteFile:
    def __init__(self, remote_path: str, local_path: str, session: requests.Session):
        self.session = session
        self.remote_path = remote_path
        self.local_path = local_path
        self.url = "http://c.pcs.baidu.com/rest/2.0/pcs/file?method=download&app_id=250528&path={path}".format(
            path=remote_path)
        self.init()

    def init(self):
        url = "http://c.pcs.baidu.com/rest/2.0/pcs/file?method=download&app_id=250528&path={path}".format(
            path=self.remote_path)
        headers = default_conf.user_agent_headers
        response = self.session.head(url, headers=default_conf.user_agent_headers)
        if response.status_code == 404:
            raise exceptions.RemoteFileNotExistException(self.remote_path)
        response_headers = response.headers
        self.file_size = int(response_headers["x-bs-file-size"])
        self.etag = response_headers["Etag"]
        self.remote_md5 = response_headers["Content-MD5"]
        block_number = self.file_size // default_conf.download_block_size
        if self.file_size % default_conf.download_block_size:
            block_number += 1
        self.to_download = [1, ] * block_number
        self.block_num = block_number
        self.temp_file_path = ".".join((self.local_path, self.remote_md5, "fktd"))

    def download(self):
        target_dir = os.path.dirname(self.local_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        f = open(self.temp_file_path, 'wb')
        self.task_queue = Queue()
        self.buff = [0, ] * self.block_num
        # worker进程完成下载后将数据通过index_and_data_queue以(index,data)的形式发送至主线程
        # worker线程无法获取任务时通过该队列发送一个(-1,None)
        # 主线程每接收到一个None就将计数器加一，直到所有worker线程退出
        self.index_and_data_queue = Queue()
        for (index, i) in enumerate(self.to_download):
            if i:
                self.task_queue.put(index)
        finished_worker_number = 0
        for i in range(default_conf.max_download_task_number):
            threading.Thread(target=self.__download_worker).start()
        while finished_worker_number < default_conf.max_download_task_number:
            index, data = self.index_and_data_queue.get()
            if index != -1:
                f.seek(index * default_conf.download_block_size)
                f.write(data)
                f.flush()
                self.buff[index] = data
                self.to_download[index] = 0
            else:
                finished_worker_number += 1
        f.close()
        if os.path.exists(self.local_path):
            os.remove(self.local_path)
        os.rename(self.temp_file_path, self.local_path)

    def __download_worker(self):
        while True:
            try:
                block_index = self.task_queue.get_nowait()
                self.__download_one_block(block_index)
            except Empty:
                break
        self.index_and_data_queue.put((-1, None))

    def __download_one_block(self, block_index):
        start = block_index * default_conf.download_block_size
        end = (block_index + 1) * default_conf.download_block_size - 1
        # 坑爹BUG2
        # 开始没有用base.user_agent_headers的copy方法
        # 瞎几把引用，浅拷贝然后下文Range的时候相互影响出错了
        headers = default_conf.user_agent_headers
        headers["Range"] = "bytes={start}-{end}".format(start=start,
                                                        end=end)
        temp_response = self.session.get(url=self.url, headers=headers)
        if temp_response.status_code == 206:
            self.index_and_data_queue.put((block_index, temp_response.content))
        else:
            base.process_remote_error_message(temp_response.text, self.remote_path)
