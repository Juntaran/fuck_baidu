
class YunPan:
    def __init__(self,
                 user_name: str,
                 password: str,
                 cookie_path: str = "cookie_file",
                 auto_save: bool = False,
                 auto_load: bool = False):
        self.log_info = LogInfo(
            user_name=user_name,
            password=password,
            cookie_path=cookie_path,
            auto_load=auto_load,
            auto_save=auto_save
        )
        self.session = self.log_info.session




