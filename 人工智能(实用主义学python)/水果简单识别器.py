# 创建一个水果识别器，根据水果的属性，判断该水果的种类 根据“近朱者赤”的原则，选取1/5的数据作为测试集

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean
from sklearn.model_selection import train_test_split

data_path = 'C:\\Users\\shine小小昱\\Desktop\\fruit_data.csv'
save_path = 'C:\\Users\\shine小小昱\\Desktop\\'

feat_cols = ['mass', 'width', 'height', 'color_score']   # 数据特征列名


def collect_data():
    """
    数据获取
    :return:
    """
    f = open(data_path, encoding='utf-8')  # 中文文件名或中文路径必须这么打开
    data_df = pd.read_csv(f, header=0)
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
    :return: 训练样本，测试样本
    """
    # 划分数据集
    train_df, test_df = train_test_split(data_df, test_size=1 / 5, random_state=3)

    return train_df, test_df


def predict_data(test_sample_feat, train_df):
    """
        预测数据   找到最近距离训练样本，取其标签作为预测样本标签
        :param test_sample_feat: 测试样本特征
        :param train_df: 训练数据
        :return: 预测标签
    """
    dis_list = []

    for idx, row in train_df.iterrows():
        train_sample_feat = row[feat_cols].values  # 带values的是返回列表形式数据 不带values是代表要操作
        dis = euclidean(test_sample_feat, train_sample_feat)
        dis_list.append(dis)

    pos = np.argmin(dis_list)
    pred_label = train_df.iloc[pos]['fruit_name']

    return pred_label


def analyze_data(train_df, test_df):
    """
    数据分析 分析预测情况
    :param train_df: 训练样本
    :param test_df: 测试样本
    :return: 预测情况
    """
    acc_count = 0

    for idx, row in test_df.iterrows():
        test_sample_feat = row[feat_cols].values   # 传入列表时需要加上values才能返回列表形式的值
        pred_label = predict_data(test_sample_feat, train_df)
        true_label = row['fruit_name']

        if pred_label == true_label:
            acc_count += 1

    accuracy = acc_count / test_df.shape[0]
    print('预测成功率为{:.2f}%'.format(accuracy * 100))

    return [acc_count, test_df.shape[0] - acc_count]



def save_and_show(pred_state):
    """
    结果展示与保存
    :return:
    """
    plt.figure()
    plt.pie(pred_state, labels=['预测成功', '预测失败'], autopct='%.2f%%',
            explode=[0, 0.05], colors=['c', 'm'], shadow=True)
    plt.title('水果识别测试')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 在matplotlib中添加中文字体    添加中文字体有可能导致特殊符号不能显示
    plt.rcParams['axes.unicode_minus'] = False  # matplotlib显示中文后导致负号异常 以此解决

    all_data_df = collect_data()
    inspect_data(all_data_df)
    train_data_df, test_data_df = process_data(all_data_df)
    predict_state = analyze_data(train_data_df, test_data_df)
    save_and_show(predict_state)
