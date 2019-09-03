# 通过盒形图可视化不同卧室个数对应的房屋价格的分布
# 通过双变量图观察卫生间个数与房屋价格的关系
# 通过热图可视化变量间的关系

# 如果有多个画图 运行程序时 每个图的show（）不能少 不然容易最后都画到一张图上面

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data_path = 'C:\\Users\\shine小小昱\\Desktop\\house_data.csv'
save_path = 'C:\\Users\\shine小小昱\\Desktop\\'


def collect_data():
    """
    载入csv数据至pandas
    :return: 所有数据df
    """
    f       = open(data_path, encoding='utf-8')      # 中文文件名或中文路径必须这么打开
    data_df = pd.read_csv(f, header=0)               # 可只读取需要的列
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


def process_data(data_df):
    """
    处理数据，去除空值
    :param data_df: 所有数据df
    :return: 去除空值后的数据
    """
    cln_data_df = data_df.dropna()
    print('原始数据有{}行记录，处理后的数据有{}行记录'.format(data_df.shape[0], cln_data_df.shape[0]))

    return cln_data_df


def analyze_by_box(df):
    """
    通过盒形图可视化不同卧室个数对应的房屋价格的分布
    :param df: 数据
    :return:
    """

    sns.boxplot(data=df, x="bedrooms", y='price')
    plt.title('Price Analysis by Bedroom')
    plt.savefig(save_path + '卧室房价盒型图.png')
    plt.show()


def analyze_dual_variables(df):
    """
    通过双变量图观察卫生间个数与房屋价格的关系
    :param df: 数据
    :return:
    """

    sns.jointplot(data=df, x='bathrooms', y='price')  # 这种画图不能加标题 不然会混乱乱
    plt.savefig(save_path + '房价卫生间变量关系.png')
    plt.show()


def analyze_variables_relationships(df):
    """
    通过热图可视化变量间的关系（基于皮尔逊相关系数：-1 到 0 到 1 ，体现正负相关强度）
    :param df:
    :return:
    """
    corr_df = df.corr()   # df对象本身具有相关性计算方法 可添加参数更改相关性计算公式 默认计算皮尔逊相关系数
    sns.heatmap(corr_df, annot=True)  # 传入相关性结果数组 调用注释 显示所有变量的两两相关性
    plt.title("Houses' Attributions Relationships")
    plt.savefig(save_path + '房价变量相关性热图.png')
    plt.show()


if __name__ == '__main__':
    all_data_df = collect_data()
    inspect_data(all_data_df)
    proc_data_arr = process_data(all_data_df)
    analyze_by_box(proc_data_arr)
    analyze_dual_variables(proc_data_arr)
    analyze_variables_relationships(proc_data_arr)