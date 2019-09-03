# 鸢尾花识别 成功率预测 饼图展示

# 机器学习基础知识 通过最近距离进行数据分类

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean
from sklearn.model_selection import train_test_split

data_path = 'C:\\Users\\shine小小昱\\Desktop\\data_ai\\Iris.csv'
save_path = 'C:\\Users\\shine小小昱\\Desktop\\'

species   = ['Iris-setosa',       # 山鸢尾
             'Iris-versicolor',   # 变色鸢尾
             'Iris-virginica'     # 维吉尼亚鸢尾
             ]
# 特征列名
feat_cols = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']


def collect_data():
    """
    数据获取
    :return:
    """
    f       = open(data_path, encoding='utf-8')         # 中文文件名或中文路径必须这么打开
    data_df = pd.read_csv(f, header=0, index_col='Id')  # 设置索引
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
    :return:训练样本， 测试样本
    """
    # 划分数据集(返回训练和测试样本)           数据      测试样本占比    随机抽取样本的方法标记
    train_df, test_df = train_test_split(data_df, test_size=1/3, random_state=10)

    return train_df, test_df


def predict_data(test_sample_feat, train_df):
    """
    预测数据   找到最近距离训练样本，取其标签作为预测样本标签
    :param test_sample_feat: 测试样本特征
    :param train_df: 训练数据
    :return: 预测标签
    """
    dis_list = []  # 和训练样本的距离列表

    for idx, row in train_df.iterrows():  # 返回索引和行值的迭代
        # 输入列名列表作为索引  返回相应列表形式的值
        train_sample_feat = row[feat_cols].values  # 训练样本的特征 带values的是返回列表形式数据 不带values是代表要操作
        dis = euclidean(test_sample_feat, train_sample_feat)  # 计算欧式距离
        dis_list.append(dis)

    pos        = np.argmin(dis_list)  # 返回最小值索引(位置)
    #                 基于df索引返回值
    pred_label = train_df.iloc[pos]['Species']  # 返回相应索引在训练样本中的标签

    return pred_label


def analyze_data(train_df, test_df):
    """
    数据分析   分析经过样本训练后对测试样本的预测情况
    :param train_df: 训练样本
    :param test_df: 测试样本
    :return: 预测准确率
    """
    acc_count = 0   # 预测准确的个数
    #                 返回索引和行的迭代
    for idx, row in test_df.iterrows():
        # 输入列名列表作为索引  返回相应列表形式的值
        test_sample_feat = row[feat_cols].values  # 测试样本的特征
        pred_label       = predict_data(test_sample_feat, train_df)  # 预测标签
        true_label       = row["Species"]  # 真实标签

        if true_label == pred_label:
            acc_count += 1

    accuracy = acc_count / test_df.shape[0]  # 准确率
    print('预测准确率为{:.2f}%'.format(accuracy * 100))  # 输出百分数

    fau_count = test_df.shape[0] - acc_count

    return [acc_count, fau_count]


def do_eda_plot_for_iris(iris_data):
    """
        对鸢尾花数据集进行简单的可视化
        参数：
            - iris_data: 鸢尾花数据集
    """
    # 定义不同品种对应的散点颜色字典
    category_color_dict = {
        'Iris-setosa':      'red',      # 山鸢尾
        'Iris-versicolor':  'blue',     # 变色鸢尾
        'Iris-virginica':   'green'     # 维吉尼亚鸢尾
    }
    # 返回画布和子图对象列表     区别于plt.subplot()
    fig, axes = plt.subplots(2, 1, figsize=(8, 8))

    #                                     迭代字典item
    for category_name, category_color in category_color_dict.items():

        # 查看对应品种的萼片长度(SepalLengthCm)和萼片宽度(SepalWidthCm)         绘制在子图一上的散点图
        iris_data[iris_data['Species'] == category_name].plot(ax=axes[0], kind='scatter',
                                                              x='SepalLengthCm', y='SepalWidthCm', label=category_name,
                                                              color=category_color)
        # 查看对应品种的花瓣长度(PetalLengthCm)和花瓣宽度(PetalWidthCm)         绘制在子图二上的散点图
        iris_data[iris_data['Species'] == category_name].plot(ax=axes[1], kind='scatter',
                                                              x='PetalLengthCm', y='PetalWidthCm', label=category_name,
                                                              color=category_color)

    axes[0].set_xlabel('Sepal Length')
    axes[0].set_ylabel('Sepal Width')
    axes[0].set_title('Sepal Length vs Sepal Width')

    axes[1].set_xlabel('Petal Length')
    axes[1].set_ylabel('Petal Width')
    axes[1].set_title('Petal Length vs Petal Width')

    plt.tight_layout()
    plt.show()


def save_and_show(pred_state):
    """
    结果展示与保存
    :return:
    """
    plt.figure()
    #       成功失败数据                                  自动百分化
    plt.pie(pred_state, labels=['预测成功', '预测失败'], autopct='%.2f%%',
            #   阴影         部分突出                青色  品红
            shadow=True, explode=(0.05, 0), colors=['c', 'm'])
    plt.title('简单鸢尾花预测测试')
    plt.axis('equal')  # 椭圆长短轴相同 即正圆
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    plt.rcParams['font.sans-serif']    = ['SimHei']  # 在matplotlib中添加中文字体    添加中文字体有可能导致特殊符号不能显示
    plt.rcParams['axes.unicode_minus'] = False       # matplotlib显示中文后导致负号异常 以此解决

    all_data_df   = collect_data()
    inspect_data(all_data_df)
    # EDA探索性数据分析（结合统计学的图形以及各种形式 最大化对数据的直觉） 其实就是可视化数据特征
    do_eda_plot_for_iris(all_data_df)
    train_data_df, test_data_df = process_data(all_data_df)
    predict_state = analyze_data(train_data_df, test_data_df)
    save_and_show(predict_state)

