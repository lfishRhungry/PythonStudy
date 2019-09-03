# 根据PM2.5值添加对应的等级，统计每年各等级的占比天数,并使用堆叠柱状图进行可视化。等级规则如下：
# 0-50: excellent（优）
# 50-100: good（良）
# 100-500: bad（污染）

import pandas as pd
import matplotlib.pyplot as plt

data_path = 'C:\\Users\\shine小小昱\\Desktop\\pm2.csv'
save_path = 'C:\\Users\\shine小小昱\\Desktop\\'


def collect_data():
    """
    数据获取
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
    :return:
    """
    data_df.dropna(inplace=True)

    return data_df


def analyze_data(proc_df):
    """
    数据分析
    :return:
    """
    # 数据分组
    proc_df['Level'] = pd.cut(proc_df['PM'], bins=[0, 50, 100, 500], labels=['bad', 'good', 'excellent'])
    # 透视分组统计
    anlz_df = pd.pivot_table(proc_df, index='Year', columns='Level', values=['Day'], aggfunc='count')

    anlz_df.fillna(0, inplace=True)

    return anlz_df


def save_and_show(anlz_df):
    """
    结果展示与保存
    :return:
    """
    # anlz_df.to_csv(save_path + '年度pm等级天数.csv')

    anlz_df['Day'].plot(kind='bar', stacked=True, title='Year PM Level Day Count', rot=0)
    plt.ylabel('day count')
    plt.tight_layout()
    plt.savefig(save_path + '年度pm等级天数统计.png')
    plt.show()


if __name__ == '__main__':
    all_data_df = collect_data()
    inspect_data(all_data_df)
    proc_data_df = process_data(all_data_df)
    analyzed_data_df = analyze_data(proc_data_df)
    save_and_show(analyzed_data_df)
