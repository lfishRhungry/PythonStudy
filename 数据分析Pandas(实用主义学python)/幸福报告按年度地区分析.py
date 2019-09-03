# 按年度、地区分析全球幸福报告

# 进行多列操作：多列排序，多列索引 多列分组  层级索引   透视表功能

import pandas as pd
import matplotlib.pyplot as plt

data_path = 'C:\\Users\\shine小小昱\\Desktop\\data_pd\\happiness_report.csv'
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
    #          多列排序      注意顺序                 传入列表数据设置各排序方式
    data_df.sort_values(['Year', 'Happiness Score'], ascending=[True, False], inplace=True)

    return data_df


def analyze_data(proc_df):
    """
    数据分析
    :return:多重分组之后的df， 透视处理之后的df
    """
    # 多重分组                         先后顺序注意            需处理的数据聚合操作    分组之后 year和region变成索引
    mul_grouped_df = proc_df.groupby(by=['Year', 'Region'])['Happiness Score'].mean()

    # 透视图（相当于间接按索引分了个组）   df对象    索引     需横向透视列(不会变成列名)  透视列下需统计的值(无论个数必须是列表，否则不会变成列名)     聚合函数：均值
    year_pivot_df  = pd.pivot_table(proc_df, index='Region', columns='Year', values=['Happiness Score', 'Economy (GDP per Capita)'], aggfunc='mean')

    return mul_grouped_df, year_pivot_df


def save_and_show(mul_grouped_df, year_pivot_df):
    """
    结果展示与保存
    :return:
    """
    mul_grouped_df.to_csv(save_path + '年度地区幸福指数.csv')
    year_pivot_df.to_csv(save_path + '地区年度幸福指数.csv')

    year_pivot_df['Happiness Score'].plot(kind='bar', title='Happiness Score')  # 数据选取一列值 但是因为有二层列 自动分组柱状图
    plt.ylabel('score')
    plt.tight_layout()
    plt.savefig(save_path + '地区年度幸福指数.png')
    plt.show()

    year_pivot_df['Economy (GDP per Capita)'].plot(kind='bar', title='Economy')
    plt.ylabel('GDP')
    plt.tight_layout()
    plt.savefig(save_path + '地区年度GDP.png')
    plt.show()


if __name__ == '__main__':
    all_data_df = collect_data()
    inspect_data(all_data_df)
    proc_data_df = process_data(all_data_df)
    data_mul_grp_df, data_yr_pv_df = analyze_data(proc_data_df)
    save_and_show(data_mul_grp_df, data_yr_pv_df)