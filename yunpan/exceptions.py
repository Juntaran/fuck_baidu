class NotSignedException(Exception):
    def __str__(self):
        return "还未登陆或者登陆已经失效"


class UnExceptedException(Exception):
    def __str__(self):
        return "我也不知道是什么引起了这个错误"


class RecodeNotExistsException(Exception):
    def __init__(self, recode_path: str):
        self.recode_path = recode_path

    def __str__(self):
        return "记录文件不存在，其路径应为{recode_path}".format(
            recode_path=self.recode_path)


class CanNotDownloadException(Exception):
    def __str__(self):
        return "本方法不支持下载文件夹"


class RemoteFileNotExistException(Exception):
    def __init__(self, remote_path: str):
        self.remote_path = remote_path

    def __str__(self):
        return "网盘上没有该文件:{remote_path}".format(remote_path=self.remote_path)


class UnExceptedRemoteError(Exception):
    def __init__(self, error_message: str):
        self.error_message = error_message

    def __str__(self):
        return "暂时还没有处理的百度网盘API错误提示，其内容为:{error_message}".format(error_message=self.error_message)


class RemoteFileHasBeenModified(Exception):
    def __str__(self):
        return "远程文件已被修改，请重新下载"

class DownloadFail(Exception):
    def __str__(self):
        return "下载未完成，请重试"