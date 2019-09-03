# 1. 添加一列diff用于比较中国环保部和美国使馆检测的PM2.5值的差异（两列数据的绝对值差）
# 2. 找出差别最大的10天的记录
# 3. 使用分组柱状图比较中国环保部和美国使馆检测的每年平均PM2.5的值
# 使用Pandas模块中的drop_na()方法清除记录中的空值。
# 要注意inplace参数的使用方法，如果在原始数据上进行操作，需使用inplace=True；
# 如果需要将结果赋值给一个新的变量，需使用inplace=False，其默认值为False

import pandas as pd
import matplotlib.pyplot as plt

data_path = 'C:\\Users\\shine小小昱\\Desktop\\Beijing_PM.csv'
save_path = 'C:\\Users\\shine小小昱\\Desktop\\'


def collect_data():
    """
    载入csv数据至pandas
    :return: 所有数据df
    """
    f       = open(data_path, encoding='utf-8')      # 中文文件名或中文路径必须这么打开
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
    处理分析数据
    :param data_df: 所有数据df
    :return: 年度中美统计均值df， 差值top10的df
    """

    # 处理空值
    cln_data_df = data_df.dropna().copy()   # 返回值基于源数据 当返回值后续要改动时，为不影响源数据，使用copy（）

    # 添加差值列 排序找出前十输出                                                绝对值方法
    cln_data_df['PM_dif'] = (cln_data_df['PM_China'] - cln_data_df['PM_US']).abs()
    top10_dif_day         = cln_data_df.sort_values(by='PM_dif', ascending=False).head(10).reset_index()
    print('差值最大的十天数据是：')
    print(top10_dif_day)

    # 按年份分组 统计中美统计pm值均值
    grouped_cln_df = cln_data_df.groupby('year')
    year_pm_mean   = grouped_cln_df[['PM_China', 'PM_US']].mean()        # 注意要加小括号 用的是方法

    return year_pm_mean, top10_dif_day


def save_and_show(year_pm_mean, top10_dif_day):
    """

    :param year_pm_mean: 年度中美统计均值df
    :param top10_dif_day: 差值top10的df
    :return:
    """

    # 保存csv                                        group过的df 已有一个索引和列名
    year_pm_mean.to_csv(save_path + '年度PM2.5均值.csv', header=['PM_Chine_mean', 'PM_US_mean'])
    top10_dif_day.to_csv(save_path + '差值top10.csv', index=False)

    # 画分组柱状图  df数据自动绘制分组柱状图
    year_pm_mean.plot(kind='bar')
    plt.xticks(rotation=0)
    plt.ylabel('PM2.5')
    plt.title('China & US Measure Comparison')
    plt.legend(loc='best')
    plt.tight_layout()

    plt.savefig(save_path + '中美PM2.5测量对比.png')
    plt.show()


if __name__ == '__main__':
    all_data_df = collect_data()
    inspect_data(all_data_df)
    year_pm_mean_df, top10_dif_day_df = process_and_analyze_data(all_data_df)
    save_and_show(year_pm_mean_df, top10_dif_day_df)