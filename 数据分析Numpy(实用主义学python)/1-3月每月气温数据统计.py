# 按月份统计气温最大值、最小值、平均值
# collect_and_process_data -> get_analysis -> save_and_show
# plot画图的标注一律用英文，否则显示不出来

import numpy as np
import matplotlib.pyplot as plt

path      = 'C:\\Users\\shine小小昱\\Desktop\\'
file_name = 'temp.csv'


def collect_and_process_data():
    """
    载入数据至np向量
    """

    file_path = path + file_name
    ripe_arr  = np.loadtxt(file_path, delimiter=',', dtype='str', skiprows=1)

    return ripe_arr



def get_analysis(arr, month):
    """
    输入月份和待分析向量，得到各月份大小值、均值的列表 以及该月份气温趋势列表
    """
    need_data      = []

    bool_arr       = arr[:, 0] == month    # 相当于二维数组，记得加逗号
    month_arr      = arr[bool_arr]
    month_pure_arr = np.core.defchararray.replace(month_arr[:, -1], ' C', '').astype('float')  # 得到该月气温向量

    need_data.append(np.min(month_pure_arr))
    need_data.append(np.max(month_pure_arr))
    need_data.append(np.mean(month_pure_arr))

    return need_data, list(month_pure_arr)


def save_and_show(list1, list2, list3, num1, num2, num3):
    """
    存储各月份分析结果并存储至csv
    """
    need_save_arr = np.array([list1, list2, list3]).transpose()
    np.savetxt('C:\\Users\\shine小小昱\\Desktop\\气温结果.csv', need_save_arr, delimiter=',',
               header='Jan, Feb, Mar', fmt='%.2f', comments='')


    """
    画图表示各月份气温趋势
    """
    plt.figure()
    plt.plot(num1, color='g', linestyle='-', marker='o', label='Jan')
    plt.plot(num2, color='r', linestyle='-', marker='o', label='Feb')
    plt.plot(num3, color='y', linestyle='-', marker='o', label='Mar')
    plt.title('Temporature of First Season')
    plt.xticks(range(31), [i + 1 for i in range(31)], rotation=-15)
    plt.xlabel('date')
    plt.ylabel('temporature')
    plt.legend(loc='best')   # 使得曲线注释采用plot当中设置的label
    plt.tight_layout()       # 紧凑型排版

    plt.savefig('C:\\Users\\shine小小昱\\Desktop\\气温趋势.png')
    plt.show()


def main():
    """
    主函数
    """
    ripe_data_arr     = collect_and_process_data()

    jan_data, jan_num = get_analysis(ripe_data_arr, '1')
    feb_data, feb_num = get_analysis(ripe_data_arr, '2')
    mar_data, mar_num = get_analysis(ripe_data_arr, '3')

    save_and_show(jan_data, feb_data, mar_data, jan_num, feb_num, mar_num)


if __name__ == '__main__':
    main()
