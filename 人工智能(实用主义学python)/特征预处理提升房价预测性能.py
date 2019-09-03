# 特征预处理 (特征工程)
# 数值型特征 最大最小归一化(scaler)
# 有序型特征 转换为有序数值
# 类别型特征 独热编码(One-Hot Encoding)

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler  # 独热编码 最大最小归一化

data_path = 'C:\\Users\\shine小小昱\\Desktop\\data_ai\\house_data.csv'
save_path = 'C:\\Users\\shine小小昱\\Desktop\\'

# 数值型特征列名列表
NUMERIC_FEAT_COLS = ['sqft_living', 'sqft_above', 'sqft_basement', 'long', 'lat']
# 类别型特征列名列表
CATEGORY_FEAT_COLS = ['waterfront']


def collect_data():
    """
    数据获取
    :return:
    """
    f = open(data_path, encoding='utf-8')  # 中文文件名或中文路径必须这么打开
    data_df = pd.read_csv(f, header=0, usecols=NUMERIC_FEAT_COLS + CATEGORY_FEAT_COLS + ['price'])
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


def process_features(X_train, X_test):
    """
    特征预处理
    :param X_train: 训练样本特征
    :param X_test: 测试样本特征
    """
    # 类别型数据特征做独热编码(One-Hot Encoding)
    # 得到编码对象           不返回稀疏矩阵
    encoder = OneHotEncoder(sparse=False)
    # 根据训练样本特征制定编码规则 并返回已编码的特征
    encoded_tr_feat = encoder.fit_transform(X_train[CATEGORY_FEAT_COLS])
    # 根据(由训练样本特征)已得到的编码规则 编码测试样本特征并返回
    encoded_te_feat = encoder.transform(X_test[CATEGORY_FEAT_COLS])

    # 数值型特征做归一化处理
    # 得到归一对象
    scaler = MinMaxScaler()
    # 根据训练样本特征制定归一化规则 并返回已归一化的特征
    scaled_tr_feat = scaler.fit_transform(X_train[NUMERIC_FEAT_COLS])
    # 根据(由训练样本特征)已得到的归一化规则 归一化测试样本特征并返回
    scaled_te_feat = scaler.transform(X_test[NUMERIC_FEAT_COLS])

    # 特征合并 运用numpy方法处理多维数组 横向合并(纵行合并用vstack)  必须以列表形式传入
    X_train_proc = np.hstack([encoded_tr_feat, scaled_tr_feat])
    # 注意 训练样本特征和测试样本特征的合并顺序要保持一致
    X_test_proc = np.hstack([encoded_te_feat, scaled_te_feat])

    return X_train_proc, X_test_proc


def process_and_analyze_data(data_df):
    """
    计算并分析特征与处理前后r2 score
    """
    # 没有values 得到df对象 样本分割之后特征预处理需要df特性将不同数组类型特征分开
    X = data_df[NUMERIC_FEAT_COLS + CATEGORY_FEAT_COLS]
    y = data_df['price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1 / 3, random_state=10)

    # 得到特征预处理之前的模型和score
    model = LinearRegression()
    model.fit(X_train, y_train)
    r2_score = model.score(X_test, y_test)
    print('特征预处理前的模型预测分数：{:.5f}'.format(r2_score))

    # 得到特征预处理之后的模型和score
    # 数据预处理
    X_train_proc, X_test_proc = process_features(X_train, X_test)
    model2 = LinearRegression()
    model2.fit(X_train_proc, y_train)
    r2_score2 = model2.score(X_test_proc, y_test)
    print('特征预处理后的模型预测分数：{:.5f}'.format(r2_score2))

    print('模型预测分数提高了：{:.2f}'.format((r2_score2 - r2_score) / r2_score * 100))


if __name__ == '__main__':

    all_data_df = collect_data()
    inspect_data(all_data_df)
    process_and_analyze_data(all_data_df)
