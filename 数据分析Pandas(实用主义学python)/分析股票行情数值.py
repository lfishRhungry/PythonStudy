# 计算指定股票的各项均线指标

# tushare金融数据获取 时序数据重采样resample 时序数据滚动统计rolling

# 用rolling求均线类似于平滑滤波器

import pandas as pd
import matplotlib.pyplot as plt
import tushare

save_path = 'C:\\Users\\shine小小昱\\Desktop\\'
stock_code = '600519'


def collect_data():
    """
    数据获取
    :return: 所有数据df
    """
    # 利用tushare获得金融数据       股票代码           开始时间              结束时间        每60分钟数据
    data_df = tushare.get_k_data(code=stock_code, start='2010-01-01', end='2018-10-01', ktype='60')

    return data_df


def inspect_data(data_df):
    """
    审查数据
    :param data_df: 所有数据df
    """
    print('数据预览：')
    print(data_df.head(10))

    print('数据基本信息：')
    print(data_df.info())

    print('数据内容统计：')
    print(data_df.describe())


def process_data(data_df):
    """
    数据处理：设置时间序列 重设索引 重采样 聚合数据 丢掉空值
    """
    # 设date列为时间序列并赋值到原数据列 设为索引 方便操作
    data_df['date'] = pd.to_datetime(data_df['date'])
    data_df.set_index('date', inplace=True)
    # 按天为单位重采样 以每天最后一个数值聚合数据
    resampled_df = data_df.resample('D').last()
    resampled_df.dropna(inplace=True)  # 在源数据上丢掉空值

    return resampled_df


def analyze_data(proc_df):
    """
    数据分析：利用rolling窗口统计 计算均线
    """
    # 增加新列             滚动统计close      窗口值5行    统计均值
    proc_df['MA 5'] = proc_df['close'].rolling(window=5).mean()
    proc_df['MA 10'] = proc_df['close'].rolling(window=10).mean()
    proc_df['MA 30'] = proc_df['close'].rolling(window=30).mean()

    return proc_df


def save_and_show(alz_df):
    """
    结果展示
    :param alz_df: 已处理分析过的数据
    """
    alz_df.to_csv(save_path + '股市收盘均线.csv')
    # 画列表输入中的列数值 自动以索引为横轴       默认画折线图
    alz_df[['close', 'MA 5', 'MA 10', 'MA 30']].plot(rot=90)
    plt.ylabel('price')
    plt.title('STOCK TREND')
    plt.savefig(save_path + '收盘价均线统计.png')
    plt.show()


if __name__ == '__main__':
    all_data_df = collect_data()
    inspect_data(all_data_df)
    proc_data_df = process_data(all_data_df)
    analyzed_data_df = analyze_data(proc_data_df)
    save_and_show(analyzed_data_df)
