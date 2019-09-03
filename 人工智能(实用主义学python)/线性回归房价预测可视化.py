# 将每个特征值与标签的关系用散点图表示 计算出r2得分
# 并画出该特征值通过线性回归模型训练得到的直线 进行可视化比较
# 回归线绘制 分组图复习

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

data_path = 'C:\\Users\\shine小小昱\\Desktop\\data_ai\\house_data.csv'
save_path = 'C:\\Users\\shine小小昱\\Desktop\\'
# 使用的特征列名列表
feat_cols = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'sqft_above', 'sqft_basement']


def collect_data():
    """
    数据获取
    :return:
    """
    f = open(data_path, encoding='utf-8')  # 中文文件名或中文路径必须这么打开
    data_df = pd.read_csv(f, header=0, usecols=feat_cols + ['price'])
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


def process_analyze_show_data(data_df):
    """
    计算每个特征r2分数 画出每个特征和标签散点图 及其回归线
    """
    # 返回画布fig和划分的子图二维列表axes     单独的plt.subplot返回一个指明位置的子图对象
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))

    for i, feat_col in enumerate(feat_cols):

        # 提取单个特征列 建立模型   特征多维数组必须是一列一列的
        X = data_df[feat_col].values.reshape(-1, 1)      # 在values操作转换为多维数组之前 在df对象状态下就已经变为一行 所以要转变
        y = data_df['price'].values                      # 标签多维数组只要是一维向量就ok
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1 / 3, random_state=10)
        model = LinearRegression()
        model.fit(X_train, y_train)
        # 回归问题得到的分数是R2形式 表示x对y的解释程度
        r2_score = model.score(X_test, y_test)
        print(f'{feat_col}特征预测的R2值：{r2_score}')

        # 拿到回归模型直线方程的权重w和截距b
        w = model.coef_
        b = model.intercept_

        # 当前子图画散点图和直线(折线图)
        # 对于子图对象或者plt而言 直方图和散点图是单独方法 柱状图和折线图是plot里面可以设置的
        axes[(i + 1) // 3 - 1, i % 3].scatter(X, y, alpha=0.5)
        axes[(i + 1) // 3 - 1, i % 3].plot(X, w * X + b, c='r')
        axes[(i + 1) // 3 - 1, i % 3].set_xlabel(f'{feat_col}')    # 子图设置横纵轴方法
        axes[(i + 1) // 3 - 1, i % 3].set_ylabel('price')
        axes[(i + 1) // 3 - 1, i % 3].set_title(f'{feat_col}预测情况')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决matplotlib中不能显示中文问题 必须先from pylib import *
    plt.rcParams['axes.unicode_minus'] = False  # matplotlib显示中文后导致负号异常 以此解决

    all_data_df = collect_data()
    inspect_data(all_data_df)
    process_analyze_show_data(all_data_df)

