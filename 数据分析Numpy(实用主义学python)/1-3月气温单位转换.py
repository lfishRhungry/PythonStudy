# 运用数据处理将csv表格文件中的摄氏度转换为华氏度
# f = 1.8 * c + 32
# collect_data -> process_data -> analyze_data -> show_results

import csv
import numpy as np


def collect_data():
    print('开始收集数据...')
    file_path = path + file_name
    arr = np.loadtxt(file_path, delimiter=',', dtype='str', skiprows=1)  # 导入成为向量
    print('收集数据完毕')
    print('-----------')
    return arr


def process_data(arr):
    print('开始处理数据...')
    arr_col = arr[:, 1]      # 取需要的第二列数据
    arr_num = np.core.defchararray.replace(arr_col, ' C', '').astype('float')  #去除不需要的字符并转换数据类型
    print('数据处理完毕')
    print('-----------')
    return arr_num


def analyze_data(arr_c):
    print('开始分析数据...')
    arr_f = 1.8 * arr_c + 32   # 数据转化为华氏度
    print('数据分析完毕')
    print('-----------')
    return arr_f


if __name__ == '__main__':
    path         = 'C:\\Users\\shine小小昱\\Desktop\\'
    file_name    = 'temp.csv'

    data_arr     = collect_data()
    arr_number   = process_data(data_arr)
    arr_number_f = analyze_data(arr_number)

    print('开始写入数据...')
    # 创建新csv文件以写入得到的数据
    with open('C:\\Users\\shine小小昱\\Desktop\\test1.csv', 'w+', encoding='utf-8') as f:
        writer = csv.writer(f)
        for i in arr_number_f:     # 写入一列
            # 数据保留两位小数并转换类型 加上必要字符串 一行一行的写入 注意是作为列表写入
            writer.writerow([str(round(i, 2)) + ' F'])   # 一行一行的写入 注意是作为列表写入
    print('数据写入完毕')
