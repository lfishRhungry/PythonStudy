# 绘制不同用户季度平均骑行时间的分组柱状图

# 分组柱状图绘制 matplotlib中文显示 matplotlib坐标轴设置

import numpy as np
import matplotlib.pyplot as plt

data_path = 'C:\\Users\\shine小小昱\\Desktop\\data\\bikeshare\\'  # 路径名注意不要写错啊
# 文件名
data_filenames = ['2017-q1_trip_history_data.csv', '2017-q2_trip_history_data.csv',
                  '2017-q3_trip_history_data.csv', '2017-q4_trip_history_data.csv']


def collect_process_analyze_data():
    """
    载入csv数据至numpy向量
    :return: 会员与非会员每季度平均骑行时间列表
    """

    mem_mean_list = []
    cas_mean_list = []

    for data_filename in data_filenames:
        data_file    = data_path + data_filename  # 拼接完整路径
        # 加载为np向量 csv数据是逗号分隔 加载数据类型是字符串 去除第一行表头
        data_arr     = np.loadtxt(data_file, delimiter=',', dtype='str', skiprows=1)
        want_arr     = np.concatenate([data_arr[:, 0].reshape(-1, 1), data_arr[:, -1].reshape(-1, 1)], axis=1)
        want_arr_cln = np.core.defchararray.replace(want_arr, '"', '')

        mem_arr      = want_arr_cln[want_arr_cln[:, 1] == 'Member']
        cas_arr      = want_arr_cln[want_arr_cln[:, 1] == 'Casual']
        mem_mean     = np.mean(mem_arr[:, 0].astype('float'))
        cas_mean     = np.mean(cas_arr[:, 0].astype('float'))

        mem_mean_list.append(mem_mean)
        cas_mean_list.append(cas_mean)

    return mem_mean_list, cas_mean_list


def save_and_show(mem_mean_list, cas_mean_list):
    """
    画分组柱状图
    :param mem_mean_list:  会员每季度平均骑行时间列表
    :param cas_mean_list: 非会员每季度平均骑行时间列表
    :return:
    """
    bar_width    = 0.35  # 柱子宽度
    bar_locs     = np.arange(4)   # 柱子横轴刻度
    xtick_labels = [f'第{i + 1}季度' for i in range(4)]  # 柱子横轴坐标标识

    plt.figure(figsize=(18, 9))
    #  位置刻度（iterate）  数据（list）     柱子宽度     柱子填充颜色   透明度      注释
    plt.bar(bar_locs, mem_mean_list, width=bar_width, color='g', alpha=0.7, label='会员')
    #        第二个柱状图横轴刻度向右移动一个柱子宽度 防止叠加
    plt.bar(bar_locs + bar_width, cas_mean_list, width=bar_width, color='r', alpha=0.7, label='非会员')
    #     重新设置刻度向右移动半个柱子宽度（居中）   刻度标识
    plt.xticks(bar_locs + bar_width / 2, xtick_labels, rotation=45)
    plt.ylabel('平均骑行时间/分钟')
    plt.title('各类用户季度平均骑行时间分组柱状图')
    plt.legend(loc='best')
    plt.tight_layout()

    plt.savefig('C:\\Users\\shine小小昱\\Desktop\\分组柱状图.png')
    plt.show()


if __name__ == '__main__':

    plt.rcParams['font.sans-serif']    = ['SimHei']    # 在matplotlib中添加中文字体
    plt.rcParams['axes.unicode_minus'] = False         # matplotlib显示中文后导致负号异常 以此解决

    member_mean_list, casual_mean_list = collect_process_analyze_data()
    save_and_show(member_mean_list, casual_mean_list)
