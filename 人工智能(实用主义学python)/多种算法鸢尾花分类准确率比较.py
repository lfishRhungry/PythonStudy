# 运用kNN 逻辑回归(logistic regression) SVM(支持向量机) 实现鸢尾花识别 比较准确率

# 遍历模型

import pandas as pd
from sklearn.model_selection import train_test_split  # 样本数据分类
from sklearn.neighbors import KNeighborsClassifier    # kNN
from sklearn.linear_model import LogisticRegression   # 逻辑回归
from sklearn.svm import SVC                           # SVM

data_path = 'C:\\Users\\shine小小昱\\Desktop\\data_ai\\Iris.csv'
save_path = 'C:\\Users\\shine小小昱\\Desktop\\'
# 特征列名
feat_cols = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']
# 标签映射表
species_label_dict = {
    'Iris-setosa':      0,  # 山鸢尾
    'Iris-versicolor':  1,  # 变色鸢尾
    'Iris-virginica':   2   # 维吉尼亚鸢尾
}


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


def process_and_analyze_data(data_df):
    """
    遍历三种分类模型 计算对应得分
    :return:
    """
    # 字符串标签映射到数字(建立新列)           按字典映射
    data_df['Label'] = data_df['Species'].map(species_label_dict)
    # 获取数据集特征
    X = data_df[feat_cols].values   # 带values的是返回列表形式数据(多维数组) 不带values返回df对象
    # 获取数据集标签
    y = data_df['Label'].values
    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1 / 3, random_state=10)

    # 建立模型对应字典 建立即创建
    model_dict = {'kNN': KNeighborsClassifier(n_neighbors=7),         # 输入k值
                  'Logistic Regression': LogisticRegression(C=1e3),   # 输入正则系数
                  'SVM': SVC(C=1e3)                                   # 输入正则系数
                  }

    # 遍历模型，计算得分并输出
    for model_name, model in model_dict.items():
        model.fit(X_train, y_train)
        acc = model.score(X_test, y_test)
        print('{}模型的预测准确率：{:.2f}%'.format(model_name, acc * 100))


if __name__ == '__main__':
    all_data_df = collect_data()
    inspect_data(all_data_df)
    process_and_analyze_data(all_data_df)
