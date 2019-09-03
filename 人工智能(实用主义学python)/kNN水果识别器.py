# 使用 scikit-learn 的 kNN 分类算法实现水果识别器

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

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


def process_and_analyze_data(data_df):
    """
    数据处理
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
    # 声明kNN模型
    model = KNeighborsClassifier()
    # (输入训练样本)训练模型
    model.fit(X_train, y_train)
    # (输入测试样本)评价模型
    accuracy = model.score(X_test, y_test)
    print('预测准确率为：{:.2f}'.format(accuracy * 100))
    # 取单个测试样本
    idx = 10
    test_sample_feat = X_test[idx, :]   # 对列表数据的操作 加[]变为列表
    y_true = y_test[idx]
    # 输入测试特征值 利用已经训练过的knn对象预测  返回列表 取出值
    # 必须以列表形式传入样本特征 返回列表形式预测值
    y_pred = model.predict([test_sample_feat])[0]
    print('真实标签为：{}\n预测标签为：{}'.format(y_true, y_pred))

    return accuracy


def save_and_show(accuracy):
    """
    结果展示与保存
    :return:
    """
    plt.figure()
    plt.pie([accuracy, 1 - accuracy], labels=['预测成功', '预测失败'], autopct='%.2f%%',
            explode=[0, 0.05], colors=['c', 'm'], shadow=True)
    plt.title('水果识别测试')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 在matplotlib中添加中文字体    添加中文字体有可能导致特殊符号不能显示
    plt.rcParams['axes.unicode_minus'] = False  # matplotlib显示中文后导致负号异常 以此解决

    all_data_df = collect_data()
    inspect_data(all_data_df)
    predict_accuracy = process_and_analyze_data(all_data_df)
    save_and_show(predict_accuracy)