from ..yunpan import YunPan

# YunPan("<用户名>", "<密码>", [auto_save=False], [auto_load=False])
the_yun_pan = YunPan("{用户名}", "{密码}", auto_load_recode=True, auto_save_recode=True)

if not the_yun_pan.has_logined:
    the_yun_pan.login()
# the_yun_pan.download_one_file(<远程路径>,[本地路径])
the_yun_pan.download_one_file("/1.mp4")
