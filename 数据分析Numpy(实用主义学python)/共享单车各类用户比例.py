# 画出各类用户比例的饼图

# 数组形状的改变 数组合并 饼图绘制

import numpy as np
import matplotlib.pyplot as plt

data_path      = 'C:\\Users\\shine小小昱\\Desktop\\data\\bikeshare\\'  # 路径名注意不要写错啊
# 文件名
data_filenames = ['2017-q1_trip_history_data.csv', '2017-q2_trip_history_data.csv',
                  '2017-q3_trip_history_data.csv', '2017-q4_trip_history_data.csv']


def collect_and_process_data():

    member_type_list = []

    for data_filename in data_filenames:
        file_path        = data_path + data_filename
        data_arr         = np.loadtxt(file_path, delimiter=',', dtype='str', skiprows=1)    # 载入arr
        # 取member一列去双引号 一列数据默认为一行 所以reshape改变形状  -1代表让函数自己算多少行
        member_type_arr  = np.core.defchararray.replace(data_arr[:, -1], '"', '').reshape(-1, 1)
        # 结果加入到到列表
        member_type_list.append(member_type_arr)

    year_member_type = np.concatenate(member_type_list)  # 将数组内的arr合并为一个 上下拼接

    return year_member_type


def analyze_data(year_member_type):
    # 过滤取出要求的数据arr 并取行数
    n_member = year_member_type[year_member_type == 'Member'].shape[0]
    n_casual = year_member_type[year_member_type == 'Casual'].shape[0]
    n_users  = [n_member, n_casual]

    return n_users


def show_and_save_data(n_users):
    plt.figure()
    # 画饼状图 传入列表数据      注释                    自动百分比        加阴影         浮现
    plt.pie(n_users, labels=['Member', 'Casual'], autopct='%.2f%%', shadow=True, explode=(0.05, 0))
    # 饼状图的长短轴设置为相同 即正圆形
    plt.axis('equal')
    # 紧凑排版
    plt.tight_layout()
    plt.savefig('C:\\Users\\shine小小昱\\Desktop\\pie_test.png')
    plt.show()


def main():
    year_member_arr = collect_and_process_data()
    n_users_list = analyze_data(year_member_arr)
    show_and_save_data(n_users_list)



if __name__ == '__main__':
    main()