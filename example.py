import yunpan

# the_yun_pan = yunpan.YunPan(<用户名>, <密码>, [auto_load=False], [auto_save=False])
the_yun_pan = yunpan.YunPan("用户名", "密码", auto_load=True, auto_save=True)
if not the_yun_pan.log_info.has_logined():
    the_yun_pan.log_info.login()

# the_yun_pan.download_one_file(<远程文件路径>,[本地路径])
the_yun_pan.download_one_file("/1.mp4")
