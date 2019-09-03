
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data_path = ''
save_path = 'C:\\Users\\shine小小昱\\Desktop\\'


def collect_data():
    """
    数据获取
    :return:
    """
    pass


def inspect_data(data_df):
    """
    审查数据
    """
    print('数据预览：')
    print(data_df.head(10))

    print('数据基本信息：')
    print(data_df.info())

    print('数据内容统计：')
    print(data_df.describe())


def process_data():
    """
    数据处理
    :return:
    """
    pass


def analyze_data():
    """
    数据分析
    :return:
    """
    pass


def save_and_show():
    """
    结果展示与保存
    :return:
    """
    pass


if __name__ == '__main__':
    pass
