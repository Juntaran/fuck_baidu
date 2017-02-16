import random
import time


# 从百度的JS里面看到的，用Python重新实现了一下
def build_gid():
    template = list("xxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx")
    for (index, the_char) in enumerate(template):
        rand_num = random.randint(0, 15)
        if the_char == 'x':
            temp_char = "%x" % rand_num
            template[index] = temp_char
        if the_char == 'y':
            rand_num = 3 & rand_num | 8
            temp_char = "%x" % rand_num
            template[index] = temp_char
    return ''.join(template).upper()


def get_time_stamp():
    return str(int(time.time() * 1000))


user_agent_headers = {
    'Referer': "https://www.baidu.com/",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
}
