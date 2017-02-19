import json
import random
import time

from src import exceptions


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


# 构建LogId的算法是看百度的JS源码得来的
# 百度JS源码经过混淆，变量名均替换成了无意义字母
# 为了省事，自己在写代码的时候使用了跟百度基本一样的变量名
def get_logid():
    u = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/~"
    the_time = time.time() * 1000
    temp_text = str(the_time) + str(random.random())
    temp_list = []
    for i in range(0, len(temp_text), 3):
        temp_list.append(temp_text[i: i + 3].encode("ASCII"))

    result = ""
    for e in temp_list:
        n = [0, 2, 1][len(e) % 3]
        e_length = len(e)
        t = e[0] << 16 | (e[1] if e_length > 1 else 0) << 8 | e[2] if e_length > 2 else 0

        o = [u[t >> 18], u[t >> 12 & 63], ord("=") if n >= 2 else u[t >> 6 & 63], ord("=") if n >= 1 else u[63 & t]]
        o = [chr(i) for i in o]
        result += "".join(o)
    result = result[:42]
    return result


def process_remote_error_message(error_text: str, remote_path: str):
    try:
        error_info = json.loads(error_text)
    except json.JSONDecodeError:
        raise exceptions.UnExceptedRemoteError(error_text)

    try:
        error_code = error_info['error_code']
        error_message = error_info['error_msg']

        if error_code == 31066:
            raise exceptions.RemoteFileNotExistException(remote_path)
        elif error_code == 31074:
            raise exceptions.CanNotDownloadException
        else:
            raise exceptions.UnExceptedRemoteError(error_message)

    except KeyError as e:
        print("属性值'{key}'不存在".format(key=e.args[0]))
