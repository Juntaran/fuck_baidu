import os


class __Conf:
    def __init__(self):
        self.download_block_size = 1024 * 1024 * 5
        self.home_path = os.path.expanduser("~")
        self.app_path = os.path.join(self.home_path, ".fuck_baidu")
        self.cookie_file_path = os.path.join(self.app_path, "cookie_file")
        self.download_info_database_file_path = os.path.join(self.app_path, "info.db")
        self.download_info_table_name = "download_infos"
        self.max_download_task_number = 5
        self.target_dir = "fuck_download"

    @property
    def user_agent_headers(self):
        return {
            'Referer': "https://www.baidu.com/",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
        }.copy()


default_conf = __Conf()
