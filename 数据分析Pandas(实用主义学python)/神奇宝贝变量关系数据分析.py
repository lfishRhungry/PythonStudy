# 比较不同类别精灵属性值分布 查看双变量数据分布 查看变量间的关系

# seaborn 盒形图 双变量图 相关系数

# 如果有多个画图 运行程序时 每个图的show（）不能少 不然容易最后都画到一张图上面

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data_path = 'C:\\Users\\shine小小昱\\Desktop\\data_pd\\pokemon.csv'
save_path = 'C:\\Users\\shine小小昱\\Desktop\\'


def collect_data():
    """
    载入csv数据至pandas
    :return: 所有数据df
    """
    f = open(data_path, encoding='utf-8')      # 中文文件名或中文路径必须这么打开
    cols = ['Name', 'Type_1', 'Total', 'HP', 'Attack', 'Defense', 'Speed', 'Height_m', 'Weight_kg', 'Catch_Rate']
    data_df = pd.read_csv(f, usecols=cols, header=0)  # 可只读取需要的列
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


def analyze_by_box(df, attr):
    """
    绘制盒型图，比较不同类别精灵属性值分布
    :param df: 数据
    :param attr: 需分析的属性
    :return:
    """
    # 自动按x分组后进行数据统计
    sns.boxplot(data=df, x='Type_1', y=attr)
    plt.title('Attribution Analysis')
    plt.xticks(rotation=90)
    plt.savefig(save_path + '精灵属性盒型图.png')
    plt.show()


def analyze_dual_variables(df, var1, var2):
    """
    双变量数据分布查看
    :param df: 数据
    :param var1: 作为变量的属性1
    :param var2: 作为变量的属性2
    :return:
    """
    # 这种画图不能加标题 不然会混乱乱
    sns.jointplot(data=df, x=var1, y=var2)
    plt.savefig(save_path + '精灵双变量属性分析.png')
    plt.show()


def analyze_variables_relationships(df):
    """
    可视化变量间相关关系（基于皮尔逊相关系数：-1 到 0 到 1 ，体现正负相关强度）
    :param df: 数据
    :return:
    """
    # 直接生成两两变量直接的相关关系形成二维数组
    corr_df = df.corr()
    #                  调用注释 方格内显示数据
    sns.heatmap(corr_df, annot=True)  # 利用seaborn生成相关关系热图
    plt.title('Attribution Relationships')

    plt.savefig(save_path + '精灵属性相关关系图.png')
    plt.show()


if __name__ == '__main__':
    all_data_df = collect_data()
    inspect_data(all_data_df)
    proc_data_df = process_data(all_data_df)
    analyze_by_box(proc_data_df, 'Attack')
    analyze_dual_variables(proc_data_df, 'Attack', 'Defense')
    analyze_variables_relationships(proc_data_df)

