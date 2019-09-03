# 比较共享单车每个季度的平均骑行时间

# numpy向量化操作 数据类型与属性 索引与切片 柱状图绘制

import numpy as np
import matplotlib.pyplot as plt

data_path = '/Users/lfish/Desktop/data/bikeshare/'  # 路径名注意不要写错啊
# 文件名
data_filenames = ['2017-q1_trip_history_data.csv', '2017-q2_trip_history_data.csv',
                  '2017-q3_trip_history_data.csv', '2017-q4_trip_history_data.csv']


def collect_data():  # 收集数据
    print('开始收集数据...')
    arr_list = []

    for data_filename in data_filenames:
        data_file = data_path + data_filename  # 拼接完整路径
        # 加载为np向量 csv数据是逗号分隔 加载数据类型是字符串 去除第一行表头
        data_arr = np.loadtxt(data_file, delimiter=',', dtype='str', skiprows=1)
        arr_list.append(data_arr)
    print('收集数据完毕')
    print('-----------')
    return arr_list  # 返回数组数据列表


def process_data(arr_list):  # 处理数据
    print('开始处理数据...')
    duration_in_min_list = []

    for data_arr in arr_list:
        duration_str_col = data_arr[:, 0]  # 取骑行时间一列数据
        # 去除双引号
        duration_in_ms = np.core.defchararray.replace(duration_str_col, '"', '')
        duration_in_min = duration_in_ms.astype('float') / 1000 / 60
        duration_in_min_list.append(duration_in_min)
    print('数据处理完毕')
    print('-----------')
    return duration_in_min_list


def analyze_data(list):
    print('开始分析数据...')
    mean_list = []

    for i, duration in enumerate(list):
        duration_mean = np.mean(duration)
        print('第{}季度的平均骑行时间：{:.2f}分钟'.format(i + 1, duration_mean))
        mean_list.append(duration_mean)
    print('数据分析完毕')
    print('-----------')
    return mean_list


def show_results(datas):  # 展示数据 画图
    print('开始画图...')
    plt.figure()  # 打开一个画布
    plt.bar(range(len(datas)), datas)  # 柱状图 横轴 纵轴 放入迭代对象
    plt.show()  # 显示
    print('图片加载完毕')


def main():
    data_arr_list = collect_data()
    duration_list = process_data(data_arr_list)
    duration_mean_list = analyze_data(duration_list)
    show_results(duration_mean_list)


if __name__ == '__main__':
    main()
