from ..src.yunpan import YunPan
from ..src.log_info import LogInfo

# YunPan("<用户名>", "<密码>", [auto_save=False], [auto_load=False])
the_yun_pan = YunPan("{用户名}", "{密码}", auto_save=True, auto_load=True)

if not the_yun_pan.log_info.has_logined:
    the_yun_pan.log_info.login()

# the_yun_pan.download_one_file(<远程路径>,[本地路径])
the_yun_pan.download_one_file("/1.mp4")
