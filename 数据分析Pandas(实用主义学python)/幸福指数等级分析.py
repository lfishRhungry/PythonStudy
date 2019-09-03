# 为幸福指数添加对应的等级

# pandas中的apply()函数 pandas中的cut()函数 透视表pd.pivot_tablt()深化 numpy表示正无限

import numpy as np
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
    data_df.sort_values(['Year', 'Happiness Score'], ascending=[True, False], inplace=True)

    return data_df


def analyze_data(proc_df):
    """
    数据分析
    """
    # # apply()向量化数据列分组操作
    # def score_level(score):   # 定义映射函数 apply自动传入列的值
    #
    #     if score <= 3:
    #         level = 'Low'
    #     elif score <= 5:
    #         level = 'Middle'
    #     else:
    #         level = 'High'
    #
    #     return level
    # # 按设定好的函数进行映射
    # proc_df['Level'] = proc_df['Happiness Score'].apply(score_level)


    # cut()对连续列数据进行分组设值
    proc_df['Level'] = pd.cut(proc_df['Happiness Score'], bins=[-np.inf, 3, 5, np.inf], labels=['Low', 'Middle', 'High'])

    # 透视表                                            多透视列构成多层索引列名     记住值要传入列表 否则没有列名索引
    anlz_df = pd.pivot_table(proc_df, index='Region', columns=['Year', 'Level'], values=['Country'],  aggfunc='count')

    anlz_df.fillna(0, inplace=True)  # 填充空值

    return anlz_df



def save_and_show(anlz_df):
    """
    结果展示与保存
    """
    anlz_df.to_csv(save_path + '幸福指数.csv')

    for year in [2015, 2016, 2017]:
        # 注意之前pandas自动将年份归为int             堆叠柱状图(选取多个列时)
        anlz_df['Country', year].plot(kind='bar', stacked=True, title=year)
        plt.ylabel('count')
        plt.legend(loc='best')
        plt.tight_layout()
        plt.savefig(save_path + f'{year}幸福指数.png')
        plt.show()


if __name__ == '__main__':
    all_data_df = collect_data()
    inspect_data(all_data_df)
    proc_data_df = process_data(all_data_df)
    analyzed_data_df = analyze_data(proc_data_df)
    save_and_show(analyzed_data_df)