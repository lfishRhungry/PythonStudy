# kNN算法鸢尾花识别 分析超参数k对分类准确率影响 分别画出两两特征的标签分界线

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

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




def collect_and_process_data():
    """
    数据获取
    :return:
    """
    f       = open(data_path, encoding='utf-8')         # 中文文件名或中文路径必须这么打开
    data_df = pd.read_csv(f, header=0, index_col='Id')  # 设置索引
    # 字符串标签映射到数字(建立新列)           按字典映射
    data_df['Label'] = data_df['Species'].map(species_label_dict)

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
    k_vals = [3, 5, 10]  # 准备分析的k值
    sel_cols = ['SepalLengthCm', 'SepalWidthCm']  # 提取两个特征 画二维标签分界线

    for k_val in k_vals:

        X = proc_df[sel_cols].values
        y = proc_df['Label'].values

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1 / 3, random_state=10)
        knn_model = KNeighborsClassifier(n_neighbors=k_val)    # 声明模型 输入k值
        knn_model.fit(X_train, y_train)   # 填充训练样本
        accuracy = knn_model.score(X_test, y_test)
        print('k = {}, accuracy = {:.2f}%'.format(k_val, accuracy * 100))


def plot_knn_boundary(knn_model, X, y, fig_title, save_fig):
    """
        绘制二维平面的kNN边界
        参数：
            knn_mode:   训练好的kNN模型
            X:          数据集特征
            y:          数据集标签
            fig_title:  图像名称
            save_fig:   保存图像的路径
    """
    h = .02  # step size in the mesh

    # Create color maps
    cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
    cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

    # 求取坐标网格mesh横纵边界 [x_min, x_max]x[y_min, y_max].
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    # 返回坐标矩阵 接受作为横纵坐标的range形式参数 返回两个相同横纵的二维数组
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    # c_是两个矩阵左右合并(按行连接) r_是两个矩阵上下合并(按列连接)
    # ravel()将数组按行拆开连接为一维数组
    Z = knn_model.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure()
    plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

    # Plot also the training points
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold,
                edgecolor='k', s=20)
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.title(fig_title)

    plt.savefig(save_fig)

    plt.show()



if __name__ == '__main__':
    process_data_df = collect_and_process_data()
    inspect_data(process_data_df)
    analyze_data(process_data_df)
