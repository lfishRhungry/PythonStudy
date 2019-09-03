"""
CSDN网页保存到本地之后 由于html文件中的一些语句 导致在本地打开时会自动跳转
将其中的onerror字符串简单的修改为on即可解决这个问题
这个代码就可以实现 在不改动原有html文件内容和路径的情况下 将更改后的新html文件放在制定的新文件夹

默认从桌面的1文件夹中提取旧html 更改后放入桌面的2文件夹

注意记得携带上相应的css文件和新html文件放在一起 不然网页结构混乱

"""

import os

# 设定旧html文件存储文件夹 已经更改处理后的新html文件存储文件夹 预先建立好文件夹
file_path = '/Users/lfish/Desktop/1/'
save_path = '/Users/lfish/Desktop/2/'


def rename_html_to_txt(file, path):
    os.rename(path + file, path + file.strip('.html') + '.txt')


def rename_txt_to_html(file, path):
    os.rename(path + file, path + file.strip('.txt') + '.html')


def rewrite_str(l):
    """
    按要求重写字符串：将字符串中的onerror改写为on
    :param l: 旧字符串
    :return: 新字符串
    """
    new_l = ''  # 新建空字符串
    indx = l.find('onerror', 0, len(l))  # 找到onerror中的第一个o在字符串中的索引

    # 遍历旧字符串的字符 如果不是error中任何一个索引的字符 就加入新字符串
    for i, char in enumerate(l):
        if i == (indx + 2) or i == (indx + 3) or i == (indx + 4) or i == (indx + 5) or i == (indx + 6):
            continue
        else:
            new_l += char

    return new_l


def rewrite_file(file, path, new_path):
    """
    按要求重写文件至新文件夹
    :param file: 文件名
    :param path: 旧路径
    :param new_path: 新文件存储路径
    """

    # 注意打开文件读写时一定要注意格式
    lines = [line for line in open(path + file, 'r', encoding='utf-8')]

    with open(new_path + file, 'w+', encoding='utf-8') as f:
        for line in lines:
            if 'onerror' in line:
                new_line = rewrite_str(line)
                f.writelines([new_line])
            else:
                f.writelines([line])


if __name__ == '__main__':

    # 运用列表解析式得到文件夹内指定html格式的文件名列表
    file_names = [file_name for file_name in os.listdir(file_path) if file_name.endswith('.html')]

    # 遍历指定html文件名 更改为txt
    for file_name in file_names:
        rename_html_to_txt(file_name, file_path)

    # 得到更改为txt格式的新的文件名列表
    new_file_names = []
    for file_name in file_names:
        new_file_names.append(file_name.strip('.html') + '.txt')

    # 遍历新txt文件名列表 重写文件至新文件夹
    for new_file_name in new_file_names:
        rewrite_file(new_file_name, file_path, save_path)

    # 遍历指定新的txt文件名 更改为html
    for new_file_name in new_file_names:
        rename_txt_to_html(new_file_name, save_path)

    # 将旧文件夹中的文件恢复原格式
    for new_file_name in new_file_names:
        rename_txt_to_html(new_file_name, file_path)

