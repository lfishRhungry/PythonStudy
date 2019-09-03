# 可视化每年PM2.5数值柱状图

import pandas as pd
import matplotlib.pyplot as plt

data_path = 'C:\\Users\\shine小小昱\\Desktop\\Beijing_PM.csv'
save_path = 'C:\\Users\\shine小小昱\\Desktop\\'


def collect_data():
    """
    载入csv数据至pandas
    :return: 所有数据df
    """
    f = open(data_path, encoding='utf-8')      # 中文文件名或中文路径必须这么打开
    data_df = pd.read_csv(f, header=0)
    return data_df


def inspect_data(data_df):
    """
    审查数据
    :param data_df: 所有数据df
    :return:
    """
    print('数据预览：')
    print(data_df.head(10))

    print('数据基本信息：')
    print(data_df.info())

    print('数据内容统计：')
    print(data_df.describe())


def process_and_analyze_data(data_df):
    """
    通过df对象groupby方法得到年度均值df
    :param data_df: 所有数据df
    :return: 年度均值df
    """
    year_grouped = data_df.groupby('year')
    year_pm_mean = year_grouped['PM_China'].mean()   # 每个按year分组的分组下pm2.5值的均值的df
    return year_pm_mean


def save_and_show(year_pm_mean):
    """
    保存csv 绘制保存柱状图
    :param year_pm_mean: 年度均值df
    :return:
    """
    #   分组操作之后的df索引自动变为分组基于的列 所以现在的df数据只有一列 用header进行列命名
    year_pm_mean.to_csv(save_path + '年度PM2.5均值统计.csv', header=['mean'])

    year_pm_mean.plot(kind='bar')
    plt.title('Year PM2.5 Mean')
    plt.ylabel('PM2.5')     # xlabel已经有名字 （即year的列明）
    plt.xticks(rotation=0)  # df对象plot默认x刻度纵向显示 设置0度旋转以激活matplotlib的横向显示
    plt.tight_layout()

    plt.savefig(save_path + '年度PM2.5均值统计.png')
    plt.show()


if __name__ == '__main__':
    all_data_df = collect_data()
    inspect_data(all_data_df)
    year_pm_mean_df = process_and_analyze_data(all_data_df)
    save_and_show(year_pm_mean_df)

