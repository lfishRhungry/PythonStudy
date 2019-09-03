# 对PM2.5值按年月两列进行统计分析,并使用分组柱状图可视化

import pandas as pd
import matplotlib.pyplot as plt

data_path = 'C:\\Users\\shine小小昱\\Desktop\\pm2.csv'
save_path = 'C:\\Users\\shine小小昱\\Desktop\\'


def collect_data():
    """
    数据获取
    :return:
    """
    f = open(data_path, encoding='utf-8')  # 中文文件名或中文路径必须这么打开
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
    数据处理
    """
    data_df.dropna(inplace=True)

    return data_df


def analyze_data(proc_df):
    """
    数据分析
    :return: 按年月多重分组后的df， 透视年列后的df
    """
    # 多重分组
    grpd_proc_df = proc_df.groupby(by=['Year', 'Month'])['PM'].mean()

    # pivot透视表                                     需横向透视列(不会变成列名)  透视列下需统计的值(无论个数必须是列表，否则不会变成列名)
    pvt_proc_df = pd.pivot_table(proc_df, index='Month', columns='Year', values=['PM'], aggfunc='mean')   # 层级列结构

    return grpd_proc_df, pvt_proc_df


def save_and_show(grpd_proc_df, pvt_proc_df):
    """
    结果展示与保存
    """
    grpd_proc_df.to_csv(save_path + '年月统计pm.csv', header=['mean pm'])
    pvt_proc_df.to_csv(save_path + '年透视图pm.csv')
    #  只有一个主列 可不指定列名
    pvt_proc_df['PM'].plot(kind='bar', title='PM2.5', rot=0)  # 数据本身只有一列值 但是因为有二层列 自动分组柱状图
    plt.ylabel('pm')
    plt.tight_layout()
    plt.savefig(save_path + 'pm分组柱状图.png')
    plt.show()


if __name__ == '__main__':
    all_data_df = collect_data()
    inspect_data(all_data_df)
    proc_data_df = process_data(all_data_df)
    grouped_proc_df, pivot_proc_df = analyze_data(proc_data_df)
    save_and_show(grouped_proc_df, pivot_proc_df)