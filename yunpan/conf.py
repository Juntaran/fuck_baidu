import os


class __Conf:
    def __init__(self):
        self.download_block_size = 1024 * 1024 * 5
        self.home_path = os.path.expanduser("~")
        self.app_path = os.path.join(self.home_path, ".fuck_baidu")
        self.recode_path = os.path.join(self.app_path, "recode")
        self.download_info_database_file_path = os.path.join(self.app_path, "info.db")
        self.download_info_table_name = "download_infos"
        self.thread_pool_size = 5
        self.target_dir = "fuck_download"
        self.poll_interval = 1
        self.__base_header = {
            'Referer': "https://www.baidu.com/",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
        }

    # 为了保证多次取出的header相互之间不干扰，此处使用装饰器
    # 是的，这也是必须要用一个类包装所有参数的原因
    @property
    def base_headers(self):
        return self.__base_header.copy()


default_conf = __Conf()
