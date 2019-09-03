# 统计1-3月气温在-10℃~10℃的天数统计直方图

import numpy as np
import matplotlib.pyplot as plt

path      = 'C:\\Users\\shine小小昱\\Desktop\\'
file_name = 'temp.csv'


def collect_and_process_data():
    """
    csv数据载入np向量， 处理数据
    :return: 气温一维向量
    """
    file_path = path + file_name
    all_data_arr = np.loadtxt(file_path, delimiter=',', dtype='str', skiprows=1)
    tem_arr = np.core.defchararray.replace(all_data_arr[:, 1], ' C', '').astype('float')

    return tem_arr


def analyze_data(tem_arr):
    """
    得到直方图统计信息
    :param tem_arr: 气温一维向量
    :return:
    """
    # 统计信息    边界信息
    tem_count, tem_edges = np.histogram(tem_arr, range=(-10, 10), bins=5)

    print(f'1-3月天气情况直方图统计信息为：{tem_count}， 直方图边界为：{tem_edges}')


def show_and_save_pic(tem_arr):
    """
    绘制并保存直方图
    :param tem_arr: 气温一维向量
    :return:
    """
    plt.figure(figsize=(10, 5))
    plt.hist(tem_arr, range=(-10, 10), bins=10)
    plt.xticks(range(-10, 11, 2))
    plt.xlabel('气温/C')
    plt.ylabel('天数')
    plt.title('1-3月气温直方图')
    plt.legend(loc='best')
    plt.tight_layout()

    plt.savefig('C:\\Users\\shine小小昱\\Desktop\\气温直方图.png')
    plt.show()


if __name__ == '__main__':

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 在matplotlib中添加中文字体
    plt.rcParams['axes.unicode_minus'] = False    # matplotlib显示中文后导致负号异常 以此解决

    temperature_arr = collect_and_process_data()
    analyze_data(temperature_arr)
    show_and_save_pic(temperature_arr)
