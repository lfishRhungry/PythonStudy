# 绘制1-3月的每月零上气温和零下气温天数的分组柱状图

import numpy as np
import matplotlib.pyplot as plt

path      = 'C:\\Users\\shine小小昱\\Desktop\\'
file_name = 'temp.csv'
save_path = 'C:\\Users\\shine小小昱\\Desktop\\'


def collect_process_analyze_data():
    """
    载入数据， 零上零下天数列表
    :return: 零上天数列表， 零下天数列表
    """
    up_list    = []
    below_list = []

    file_path = path + file_name
    all_data_arr = np.loadtxt(file_path, delimiter=',', dtype='str', skiprows=1)

    # 过滤得到相应月份数据向量
    jan_arr = all_data_arr[all_data_arr[:, 0] == '1']
    feb_arr = all_data_arr[all_data_arr[:, 0] == '2']
    mar_arr = all_data_arr[all_data_arr[:, 0] == '3']

    # 通过函数得到相应月份零上零下天数
    jan_up_zero_count, jan_below_zero_count = get_count(jan_arr)
    feb_up_zero_count, feb_below_zero_count = get_count(feb_arr)
    mar_up_zero_count, mar_below_zero_count = get_count(mar_arr)

    # 数据分别假如列表
    up_list.extend([jan_up_zero_count, feb_up_zero_count, mar_up_zero_count])
    below_list.extend([jan_below_zero_count, feb_below_zero_count, mar_below_zero_count])

    return up_list, below_list


def get_count(month_arr):
    """
    获取相应月份零上零下天数
    :param month_arr: 过滤出的相应月份数据向量
    :return: 零上天数， 零下天数
    """
    # 先获取相应月份温度纯数据列向量
    month_tem_arr          = np.core.defchararray.replace(month_arr[:, 1], ' C', '').astype('float').reshape(-1, 1)
    month_up_zero_count    = month_tem_arr[month_tem_arr >= 0].shape[0]  # 过滤得到行形状（个数） 待过滤向量与布尔向量维度相一致
    month_below_zero_count = month_arr.shape[0] - month_up_zero_count

    return month_up_zero_count, month_below_zero_count


def save_and_show(up_list, below_list):
    """
    画分组柱状图
    :param up_list:    零上天数列表
    :param below_list: 零下天数列表
    :return:
    """
    bar_width    = 0.25
    bar_locs     = np.arange(3)    # 横轴刻度
    xticks_label = [f'{i + 1}月份' for i in range(3)]  # 横轴刻度标识

    plt.figure(figsize=(18, 9))
    plt.bar(bar_locs, up_list, width=bar_width, color='r', label='零上天数')
    plt.bar(bar_locs + bar_width, below_list, width=bar_width, color='b', label='零下天数')  # 注意横向右移一个柱子宽度
    plt.xticks(bar_locs + bar_width / 2, xticks_label, rotation=30)  # 重新设置横轴刻度时要右移半个柱子宽度
    plt.ylabel('天数')
    plt.title('1-3月零上零下气温天数对比图')
    plt.legend(loc='best')
    plt.tight_layout()

    plt.savefig(save_path + '气温对比图.png')
    plt.show()


if __name__ == '__main__':

    plt.rcParams['font.sans-serif']     = ['SimHei']    # 在matplotlib中添加中文字体
    plt.rcParams['axes.unicode_minus']  = False         # matplotlib显示中文后导致负号异常 以此解决

    up_zero_list, below_zero_list = collect_process_analyze_data()
    save_and_show(up_zero_list, below_zero_list)