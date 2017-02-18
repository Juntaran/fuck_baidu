class NotSignedException(Exception):
    def __str__(self):
        return "老哥，你没有登陆或者登陆已经失效"


class UnExceptedException(Exception):
    def __str__(self):
        return "我也不知道是什么引起了这个错误"


class CookieFileNotExistsException(Exception):
    def __init__(self, cookie_file_path: str):
        self.cookie_file_path = cookie_file_path

    def __str__(self):
        return "cookie file is not exists, the path should be:{cookie_file_path}".format(
            cookie_file_path=self.cookie_file_path)
