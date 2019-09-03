# 题目描述：为模型选择最优的参数并进行水果类型识别，模型包括kNN，逻辑回归及SVM。对应的超参数为：
# kNN中的近邻个数n_neighbors及闵式距离的p值
# 逻辑回归的正则项系数C值
# SVM的正则项系数C值
# 使用3折交叉验证对模型进行调参

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV  # 样本数据分类 网格搜索
from sklearn.neighbors import KNeighborsClassifier                  # kNN
from sklearn.linear_model import LogisticRegression                 # 逻辑回归
from sklearn.svm import SVC                                         # SVM

data_path = 'C:\\Users\\shine小小昱\\Desktop\\fruit_data.csv'
save_path = 'C:\\Users\\shine小小昱\\Desktop\\'
# 特征列名
feat_cols = ['mass', 'width', 'height', 'color_score']   # 数据特征列名
# 标签映射表
species_label_dict = {
    'apple':    0,
    'orange':   1,
    'lemon':    2,
    'mandarin': 3
}


def collect_data():
    """
    数据获取
    :return:
    """
    f       = open(data_path, encoding='utf-8')         # 中文文件名或中文路径必须这么打开
    data_df = pd.read_csv(f, header=0)  # 设置索引
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


def process_and_analyze_data(data_df):
    """
    遍历三种分类模型 计算对应得分
    :return:
    """
    # 字符串标签映射到数字(建立新列)           按字典映射
    data_df['Label'] = data_df['fruit_name'].map(species_label_dict)
    # 获取数据集特征
    X = data_df[feat_cols].values   # 带values的是返回列表形式数据 不带values是代表要操作
    # 获取数据集标签
    y = data_df['Label'].values
    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1 / 5, random_state=10)

    # 模型及需要交叉验证的参数名的字典包含数据列表 建立即创建
    model_dict = {'kNN': (KNeighborsClassifier(),
                          {'n_neighbors': [3, 5, 7, 9, 12, 15, 18, 20],  # k值
                           'p': [1, 2, 3, 4]}                            # 闵氏距离的参数p
                          ),
                  'Logistic Regression': (LogisticRegression(),
                                          {'C': [1e-2, 1, 1e2]}          # 正则项系数
                                          ),
                  'SVM': (SVC(),
                          {'C': [1e-2, 1, 1e2]}                          # 正则项系数
                          )
                  }

    #    模型名称    模型对象 模型需验证的参数字典及对应数据列表
    for model_name, (model, model_params) in model_dict.items():

        # 建立网格搜索对象      模型            超参数配置(字典)         5folds
        clf = GridSearchCV(estimator=model, param_grid=model_params, cv=3)
        clf.fit(X_train, y_train)   # 利用训练样本交叉验证
        best_model = clf.best_estimator_      # 得到最佳模型

        acc = best_model.score(X_test, y_test)
        print('{}模型的最佳预测准确率：{:.2f}%'.format(model_name, acc * 100))

        # 输出最优模型的超参数配置
        print('{}模型的最优参数配置为：{}'.format(model_name, clf.best_params_))


if __name__ == '__main__':
    all_data_df = collect_data()
    inspect_data(all_data_df)
    process_and_analyze_data(all_data_df)