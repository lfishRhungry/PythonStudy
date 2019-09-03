# 将制定文件夹内相同内容的文件夹删除 只保留一个
# 删除重复文件 一个文档里面两个文件夹里都有图片
# 当使用列表时 做循环要慎用索引 可能有同名混乱

import filecmp
import os

path1 = 'C:\\Users\\shine小小昱\\Desktop\\problem3_files\\pic1'
path2 = 'C:\\Users\\shine小小昱\\Desktop\\problem3_files\\pic2'

files1 = os.listdir(path1)                                # 列出path1文件列表并组合为绝对路径列表

for f in files1:
    files1[files1.index(f)] = path1 + '\\' + f

files2 = os.listdir(path2)                                # 同path1一样

for f in files2:
    files2[files2.index(f)] = path2 + '\\' + f

files    = files1 + files2                                # 合并为一个列表
file_cmp = [0]*len(files)                                 # 建立对应的标记列表 1表示标记
# 开始双重循环对比
for i in range(len(file_cmp)):                            # 单独用range数字作为循环索引，避免文件名相同时反求索引产生混论
    if not file_cmp[i]:                                   # 已标记则跳过
        for r in range(i+1, len(file_cmp)):               # 二重循环从一层之后的索引开始，避免重复，注意range值设定
            if not file_cmp[r]:                           # 同样 已标记跳过
                if filecmp.cmp(files[i], files[r]):       # 对比内容
                    file_cmp[r] = 1                       # 相同则标记

for i in range(len(file_cmp)):                            # 同样使用外部数字循环作为索引，避免混论
    if file_cmp[i]:
        os.remove(files[i])                               # 删除标记文件

