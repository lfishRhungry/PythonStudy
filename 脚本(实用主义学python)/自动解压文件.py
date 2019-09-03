# 指定文件夹内实时解压文件并删除原文件
# 扫描并选择文件——解压——删除压缩文件

import os
import shutil
import time

try:
    path  = input('请输入文件夹路径：')
    files = os.listdir(path)

except OSError:
    print('路径输入错误')

else:

    def scan_file(tar_path):          # 扫描并返回压缩文件列表 由于使用了时间刷新 所以传出文件列表每一次刷新都批量处理
        f2 = []
        for f1 in os.listdir(tar_path):
            if f1.endswith('zip'):            # ‘一个一个’地处理
                f2.append(f1)
        return f2


    def un_zip(zip_file, new_folder):         # 输入zip路径和创建的文件夹路径并解压至
        shutil.unpack_archive(zip_file, new_folder)


    def delete_zip(zip_file):                 # 删除原压缩文件
        os.remove(zip_file)


    while True:                               # 实时扫描 一直运行
        zips = scan_file(path)                # 扫描出需解压文件才解压

        if zips:

            for zip in zips:
                file_name = path + '\\\\' + zip
                folder_name = path + '\\\\' + str(zip).split('.')[0]
                os.mkdir(folder_name)
                un_zip(file_name, folder_name)
                delete_zip(file_name)

        time.sleep(5)                         # 每五秒批量处理一次
