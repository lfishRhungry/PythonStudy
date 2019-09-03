# 合并三个月气温数据 将零上和零下气温画成饼状图

import numpy as np
import matplotlib.pyplot as plt

path      = 'C:\\Users\\shine小小昱\\Desktop\\'
file_name = 'temp.csv'


def collect_and_process_data():

    file_path    = path + file_name
    all_data_arr = np.loadtxt(file_path, delimiter=',', dtype='str', skiprows=1)
    t_arr        = np.core.defchararray.replace(all_data_arr[:, -1], ' C', '').astype('float')
    # 一维数据默认为一行 调整为一列
    t_arr.reshape(-1, 1)
    return t_arr


def analyze_data(t_arr):
    t_data_list = []
    n_up_0      = t_arr[t_arr >= 0].shape[0]   # 过滤之后取行数
    n_below_0   = t_arr[t_arr < 0].shape[0]

    t_data_list.extend([n_up_0, n_below_0])
    return t_data_list


def show_and_save_data(t_data_list):
    plt.figure()
    plt.title('Temperature')
    #     数据（列表封装）   每个饼的标记                 饼图标注形式        阴影            每个饼的偏移量    饼颜色
    plt.pie(t_data_list, labels=['up-0', 'below-0'], autopct='%.2f%%', shadow=True, explode=(0.05, 0), colors=['r', 'b'])
    plt.axis('equal')  # 椭圆长短轴相同 即正圆
    plt.tight_layout()  # 紧凑排版

    plt.savefig('C:\\Users\\shine小小昱\\Desktop\\Temperature_test.png')
    plt.show()


def main():
    temperature_arr = collect_and_process_data()
    temperature_data_list  = analyze_data(temperature_arr)
    show_and_save_data(temperature_data_list)


if __name__ == '__main__':
    main()
