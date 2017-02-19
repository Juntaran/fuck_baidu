import os
from . import yunpan_recode, exceptions
from .conf import default_conf
from .yunpan_download import RemoteFile


class YunPan:
    def __init__(self,
                 user_name: str,
                 password: str,
                 recode_path: str = default_conf.recode_path,
                 auto_load_recode: bool = False,
                 auto_save_recode: bool = False):
        self.__log_info = yunpan_recode.LoginRecode(
            user_name=user_name,
            password=password,
            recode_path=default_conf.recode_path,
            auto_save_recode=auto_save_recode,
            auto_load_recode=auto_load_recode
        )
        self.__session = self.__log_info.session

    # 登陆部分开始
    def login(self):
        return self.__log_info.login()

    def save_login_recode(self):
        return self.__log_info.save()

    def load_login_recode(self):
        return self.__log_info.load()

    @property
    def has_logined(self):
        return self.__log_info.has_logined()

    def assert_logined(self):
        return self.__log_info.assert_logined()

    # 登陆部分结束

    # 下载部分开始
    def download_one_file(self, remote_path: str, local_path: str = None):
        self.__log_info.assert_logined()
        if "/" not in remote_path or not remote_path.startswith("/"):
            raise exceptions.RemoteFileNotExistException(remote_path)
        if remote_path.endswith("/"):
            raise exceptions.CanNotDownloadException
        if local_path is None:
            local_path = os.path.join(default_conf.target_dir, remote_path.split("/")[-1])

        the_remote_file = RemoteFile(remote_path, self.__session)
        the_remote_file.download_to(local_path)

    # 下载部分结束
