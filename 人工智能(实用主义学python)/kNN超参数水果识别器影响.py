# 使用不同的k值，观察对水果识别器的影响
# 使用k=1, 3, 5, 7观察对结果的影响

import pandas as pd
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



def collect_and_process_data():
    """
    数据获取
    :return:
    """
    f       = open(data_path, encoding='utf-8')         # 中文文件名或中文路径必须这么打开
    data_df = pd.read_csv(f, header=0)  # 设置索引
    # 字符串标签映射到数字(建立新列)           按字典映射
    data_df['Label'] = data_df['fruit_name'].map(species_label_dict)

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


def analyze_data(proc_df):
    """
    分析数据 不同k值对模型影响
    :param proc_df: 处理好的数据
    :return:
    """
    k_vals = [1, 3, 5, 7]  # 准备分析的k值
    sel_cols = ['mass', 'color_score']  # 提取两个特征 画二维标签分界线

    for k_val in k_vals:

        X = proc_df[sel_cols].values
        y = proc_df['Label'].values

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1 / 3, random_state=10)
        knn_model = KNeighborsClassifier(n_neighbors=k_val)    # 声明模型 输入k值
        knn_model.fit(X_train, y_train)   # 填充训练样本
        accuracy = knn_model.score(X_test, y_test)
        print('k = {}, accuracy = {:.2f}%'.format(k_val, accuracy * 100))


if __name__ == '__main__':
    process_data_df = collect_and_process_data()
    inspect_data(process_data_df)
    analyze_data(process_data_df)
