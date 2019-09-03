# 凯撒密码（Caesar cipher） 加密解密的实现


def caesar_cipher_translation(content, step_key):
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


if __name__ == '__main__':
    while True:
        raw_content = input('请输入字符串：\n')
        step = int(input('请输入钥匙：\n'))     # 注意转换数据类型
        ripe_content = caesar_cipher_translation(raw_content, step)
        print('已用凯撒密码处理得到的新字符串为：')
        print('----------------------------------------------')
        print(ripe_content)
        print('----------------------------------------------')
