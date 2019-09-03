"""
一些杂七杂八的小工具：

    sleep_and_count_time(secs)：执行程序休眠状态的同时打印报时

    str_is_number(str)：判断字符串是否为数字或浮点数

    Caesar_cipher_translation(content, step_key)：用凯撒密码的处理方式处理英文字符（可包含标点符号等）用于加密或者解密

"""

import time


def sleep_and_count_time(secs):
    """
    执行程序休眠状态的同时打印报时
    :param secs: 执行程序时需要休眠的秒数
    """
    for i in range(secs):
        print(f'请等待{secs - i}秒...')
        time.sleep(1)


def str_is_number(str):
    """
    判断字符串是否为数字或浮点数
    :param str: 字符串
    :return: True or False
    """
    try:
        if str == 'NaN':
            return False
        float(str)
        return True
    except ValueError:
        return False


def Caesar_cipher_translation(content, step_key):
    """
    用凯撒密码的处理方式处理英文字符（可包含标点符号等）
    用于加密或者解密
    密钥可以是正负整数
    整数加密钥匙取负数即是相应的解密钥匙
    :param content: 待加密（解密）字符串内容
    :param step_key: 加密（解密）钥匙 为正负正整数
    :return: 已加密（解密）的字符串
    """
    new_content = ''   # 建立空的新字符串变量u

    # 遍历待处理字符串的字符
    for char in content:
        char_unicode = ord(char)  # 转换为Unicode码

        # 判断是大写英文字母还是小写英文字母 还是其他字符 并作相应处理得到新字符unicode码
        if 65 <= char_unicode <= 90:
            new_char_unicode = (char_unicode - 65 + step_key) % 26 + 65

        elif 97 <= char_unicode <= 122:
            new_char_unicode = (char_unicode - 97 + step_key) % 26 + 97

        else:
            new_char_unicode = char_unicode

        new_content += chr(new_char_unicode)  # 转换新的Unicode码得到相应字符 将新字符加入新字符串变量

    return new_content
