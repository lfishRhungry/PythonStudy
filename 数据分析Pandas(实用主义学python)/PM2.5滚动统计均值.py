# 滚动统计PM2.5指标的3周均值、5周均值、7周均值，并对结果进行可视化

import pandas as pd
import matplotlib.pyplot as plt

data_path = 'C:\\Users\\shine小小昱\\Desktop\\pm1.csv'
save_path = 'C:\\Users\\shine小小昱\\Desktop\\'


def collect_data():
    """
    数据获取
    """
    f       = open(data_path, encoding='utf-8')  # 中文文件名或中文路径必须这么打开
    data_df = pd.read_csv(f, header=0)  # 列名采用第一行
    return data_df


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


def process_data(data_df):
    """
    数据处理：去空值以防万一 设置时间序列 重设索引 重采样 再去空值 以防万一
    """
    data_df.dropna(inplace=True)
    data_df['Timestamp'] = pd.to_datetime(data_df['Timestamp'])
    data_df.set_index('Timestamp', inplace=True)
    proc_df = data_df.resample('W').last()  # 按周为频率重采样
    proc_df.dropna(inplace=True)

    return proc_df


def analyze_data(proc_df):
    """
    数据分析  滚动统计
    :return:
    """
    proc_df['3W mean'] = proc_df['PM'].rolling(window=3).mean()
    proc_df['5W mean'] = proc_df['PM'].rolling(window=5).mean()
    proc_df['7W mean'] = proc_df['PM'].rolling(window=7).mean()

    return proc_df


def save_and_show(anlz_df):
    """
    结果展示
    :return:
    """
    # anlz_df.to_csv(save_path + 'PM2.5均线统计.csv')

    anlz_df[['PM', '3W mean', '5W mean', '7W mean']].plot()
    plt.title('PM2.5 mean')
    plt.tight_layout()
    plt.legend(loc='best')
    plt.savefig(save_path + 'PM2.5均线统计.png')
    plt.show()


if __name__ == '__main__':
    all_data_df = collect_data()
    inspect_data(all_data_df)
    proc_data_df = process_data(all_data_df)
    analyzed_data_df = analyze_data(proc_data_df)
    save_and_show(analyzed_data_df)
