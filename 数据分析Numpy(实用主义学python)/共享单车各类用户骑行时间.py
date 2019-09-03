# 比较共享单车会员与非会员用户的四个季度平均骑行时间趋势
# MemoryError 内存不够？？？？

# 布尔型数组及数据过滤 多维数组构造 折线图绘制

import numpy as np
import matplotlib.pyplot as plt

data_path = 'C:\\Users\\shine小小昱\\Desktop\\data\\bikeshare\\'  # 路径名注意不要写错啊
# 文件名
data_filenames = ['2017-q1_trip_history_data.csv', '2017-q2_trip_history_data.csv',
                  '2017-q3_trip_history_data.csv', '2017-q4_trip_history_data.csv']


def collect_and_process_data():  # 收集处理数据
    print('开始收集处理数据...')
    arr_list = []

    for data_filename in data_filenames:
        data_file = data_path + data_filename  # 拼接完整路径
        # 加载为np向量 csv数据是逗号分隔 加载数据类型是字符串 去除第一行表头
        data_arr = np.loadtxt(data_file, delimiter=',', dtype='str', skiprows=1)
        data_arr_cln = np.core.defchararray.replace(data_arr, '"', '')  # 去除双引号
        arr_list.append(data_arr_cln)
    print('收集处理数据完毕')
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


def get_mean_duration_by_type(list, member_type):  # 输入去除引号的原始数据和需要的人员类别 得到此类别每季度平均骑行时间
    mean_list = []
    for data in list:
        bool_arr = data[:, -1] == member_type
        filter_arr = data[bool_arr]
        mean_data = np.mean(filter_arr[:, 0].astype('float')/1000.60)
        mean_list.append(mean_data)
    return mean_list


def save_and_show_results(member_list, casual_list):  # 展示数据 画图

    """
    打印结果
    """
    for i in range(len(member_list)):
        member_mean = member_list[i]
        casual_mean = casual_list[i]
        print('第{}个季度，会员平均骑行时长：{:.2f}分钟，非会员平均骑行时长：{:.2f}分钟'.format(i + 1, member_mean, casual_mean))


    """
    保存结果
    """
    mean_duration_arr = np.array([member_list, casual_list]).transpose()
    np.savetxt('C:\\Users\\shine小小昱\\Desktop\\数据测试.csv', mean_duration_arr, delimiter=',',
               header='Member Mean Duration, Casual Mean Duration', fmt='%.4f', comments='')


    """
    可视化结果保存
    """
    plt.figure()
    plt.plot(member_list, color='g', linestyle='-', marker='o', label='Member')
    plt.plot(casual_list, color='r', linestyle='--', marker='*', label='Casual')
    plt.title('Member VS Casual')
    plt.xticks(range(4), ['1st', '2nd', '3rd', '4th'], rotation=45)
    plt.xlabel('Quarter')
    plt.ylabel('Mean duration(min)')
    plt.legend(loc='best')
    plt.tight_layout()

    plt.savefig('C:\\Users\\shine小小昱\\Desktop\\data_test.png')
    plt.show()



def main():
    data_arr_list = collect_and_process_data()
    print('开始计算各类用户平均骑行时间...')
    member_mean_duration_list = get_mean_duration_by_type(data_arr_list, 'Member')
    casual_mean_duration_list = get_mean_duration_by_type(data_arr_list, 'Casual')
    print('计算完毕')
    print('-----------')
    print('开始打印、保存、展示数据...')
    save_and_show_results(member_mean_duration_list, casual_mean_duration_list)
    print('全部执行完毕')


if __name__ == '__main__':
    main()
