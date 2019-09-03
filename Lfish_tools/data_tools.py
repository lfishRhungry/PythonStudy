"""
关于数据处理的一些小工具（Numpy Pandas Matplotlib）：

    inspect_df_data(data_df)：审查数据

    matplotlib_show_CHN()：使matplotlib作图可显示中文

"""

import matplotlib.pyplot as plt


def inspect_df_data(data_df):
    """
    审查数据
    :param data_df: pd的dataframe类型数据
    :return:
    """
    print('数据预览：')
    print(data_df.head(10))

    print('数据基本信息：')
    print(data_df.info())

    print('数据内容统计：')
    print(data_df.describe())


def matplotlib_show_CHN():
    """
    使matplotlib作图可显示中文
    """
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决matplotlib中不能显示中文问题 必须先from pylib import *
    plt.rcParams['axes.unicode_minus'] = False  # matplotlib显示中文后导致负号异常 以此解决