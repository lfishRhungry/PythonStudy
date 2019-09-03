# 指定文件夹内文件数大于5时 压缩文件并并删除原文件
# 扫描大于五——压缩至文件夹——删除原文件

import os
import shutil
import time

path = input('请输入文件夹路径：')
count = 0                          # 文件名计数器


def scan_file(path1):                         # 扫描非压缩文件并在大于等于三是返回文件列表
    f1 = []

    for fs in os.listdir(path1):
        if not fs.endswith('zip'):
            f1.append(fs)

    if len(f1) >= 3:
        return f1


def pack(path1, f1):                              # 压缩函数
    shutil.make_archive(path1, 'zip', f1)         # 其中压缩文件名称是path1+'zip'


while True:         # 重复执行
    files = scan_file(path)

    if files:        # 当有大于等于三文件时执行
        count += 1
        zip_path = path + '\\\\archive' + str(count)
        file_path = path + '\\\\new'                   # 新建一个临时文件夹将待压缩文件放入
        os.mkdir(file_path)

        for f in files:
            shutil.move(path + '\\\\' + f, file_path)
        pack(zip_path, file_path)

        for f in os.listdir(file_path):                  # 删除文件夹内已压缩的文件
            os.remove(file_path + '\\\\' + f)

        os.rmdir(file_path)                              # 删除新建的临时文件夹

    time.sleep(5)                                        # 定时执行循环扫描操作 防止文件还没传完进文件夹就被压缩了
