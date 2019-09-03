# 统计会员与非会员用户骑行时间 并分别绘制直方图

# 数据合并轴方向 numpy直方图 matplotlib绘制直方图 子图绘制

import numpy as np
import matplotlib.pylab as plt

data_path = 'C:\\Users\\shine小小昱\\Desktop\\data\\bikeshare\\'  # 路径名注意不要写错啊
# 文件名
data_filenames = ['2017-q1_trip_history_data.csv', '2017-q2_trip_history_data.csv',
                  '2017-q3_trip_history_data.csv', '2017-q4_trip_history_data.csv']


def collect_and_process_data():
    """
    收集、处理数据
    :return: 全年骑行时间和用户的二维向量
    """
    arr_list =[]

    for data_filename in data_filenames:
        data_file    = data_path + data_filename  # 拼接完整路径
        data_arr     = np.loadtxt(data_file, delimiter=',', dtype='str', skiprows=1)
        want_arr     = np.concatenate([data_arr[:, 0].reshape(-1, 1), data_arr[:, -1].reshape(-1, 1)], axis=1)  # 横向合并
        cln_want_arr = np.core.defchararray.replace(want_arr, '"', '')  # 去除双引号
        arr_list.append(cln_want_arr)

    year_arr = np.concatenate(arr_list, axis=0)  # 纵向合并
    return year_arr


def analyze_data(year_arr):
    """
    分析数据 输出各类用户直方图数据
    :param year_arr: 全年骑行数据向量
    :return: 各类用户的骑行时间一维向量
    """
    member_arr = year_arr[year_arr[:, 1] == 'Member']
    casual_arr = year_arr[year_arr[:, 1] == 'Casual']
    member_dur = member_arr[:, 0].astype('float') / 1000 / 60
    casual_dur = casual_arr[:, 0].astype('float') / 1000 / 60

    #                                     待处理数据    需取出的范围      多少份
    m_dur_hist, m_dur_edges = np.histogram(member_dur, range=(0, 180), bins=12)  # 得到直方图数据列表和边界数据列表
    c_dur_hist, c_dur_edges = np.histogram(casual_dur, range=(0, 180), bins=12)

    print(f'会员直方图统计信息：{m_dur_hist}  会员直方图边界：{m_dur_edges}')
    print(f'非会员直方图统计信息：{c_dur_hist}  非会员直方图边界：{c_dur_edges}')

    return member_dur, casual_dur


def show_data(member_dur, casual_dur):
    """
    在同一画布画出各用户直方图
    :param member_dur: 会员骑行时间一维向量
    :param casual_dur: 非会员骑行时间一维向量
    :return:
    """
    fig = plt.figure(figsize=(10, 5))   # 输入画布大小参数
    ax1 = fig.add_subplot(1, 2, 1)      # 实例化一个画布上的一个子图
    ax2 = fig.add_subplot(1, 2, 2, sharey=ax1)    # 共用一个y轴

    ax1.hist(member_dur, range=(0, 180), bins=12)   # 画直方图
    ax1.set_xticks(range(0, 181, 15))               # x轴刻度设置
    ax1.set_title('Member')
    ax1.set_xlabel('Min')
    ax1.set_ylabel('Count')

    ax2.hist(casual_dur, range=(0, 180), bins=12)
    ax2.set_xticks(range(0, 181, 15))
    ax2.set_title('Casual')
    ax2.set_xlabel('min')
    ax2.set_ylabel('Count')

    plt.tight_layout()
    plt.savefig('C:\\Users\\shine小小昱\\Desktop\\直方图.png')
    plt.show()


if __name__ == '__main__':
    year_arr_list = collect_and_process_data()
    member_dur_list, casual_dur_list = analyze_data(year_arr_list)
    show_data(member_dur_list, casual_dur_list)
