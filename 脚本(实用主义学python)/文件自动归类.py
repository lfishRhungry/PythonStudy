# 将指定文件夹内的文件按后缀名分类并移动到创建的相应文件夹

import os
import shutil

try:
    path  = input('请填写文件夹绝对路径：（如：C:\\Users\\shine小小昱\\Desktop）\n')
    files = os.listdir(path)

except OSError:
    print('路径输入错误！')                             # 防止用户输入错误路径，使用try\except\else语句

else:

    for f in files:
        folder_name = path + '\\\\' + f.split('.')[-1]   # 假定存在的文件夹名称
        file_name   = path + '\\\\' + f                    # 文件名称绝对路径 用来指代文件本身

        if f != '文件自动归类.py':                       # 排除将代码文件自身也归类

            if os.path.exists(folder_name):
                shutil.move(file_name, folder_name)
            else:
                os.makedirs(folder_name)
                shutil.move(file_name, folder_name)