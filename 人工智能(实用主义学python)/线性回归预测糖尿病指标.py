# 使用scikit-learn的线型回归模型对糖尿病的指标值进行预测
# 选取1/5的数据作为测试集

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

data_path = 'C:\\Users\\shine小小昱\\Desktop\\diabetes.csv'
save_path = 'C:\\Users\\shine小小昱\\Desktop\\'
# 使用的特征列名列表
feat_cols = ['AGE', 'SEX', 'BMI', 'BP']


def collect_data():
    """
    数据获取
    :return:
    """
    f = open(data_path, encoding='utf-8')  # 中文文件名或中文路径必须这么打开
    data_df = pd.read_csv(f, header=0, usecols=feat_cols + ['Y'])
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


def plot_feat_and_price(data_df):
    """
        绘制每列特征与房价的关系
        参数：
            -house_data: 房屋价格数据集
    """
    # 采用的特征
    feat_cols = ['AGE', 'SEX', 'BMI', 'BP']
    # 返回画布fig和划分的子图列表axes
    fig, axes = plt.subplots(2, 2, figsize=(15, 8))
    for i, feat_col in enumerate(feat_cols):
        # 提取画图需要的一个特征列和标签列  画散点图你                                     标明画在哪一个子图上
        data_df.plot.scatter(x=feat_col, y='Y', alpha=0.5, ax=axes[i // 2, (i + 1) % 2 - 1])
    plt.tight_layout()
    plt.show()


def process_and_analyze_data(data_df):
    """
    分析处理数据
    """
    X = data_df[feat_cols].values
    y = data_df['Y'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1 / 5, random_state=10)
    # 建立线性回归模型
    model = LinearRegression()
    model.fit(X_train, y_train)
    # 回归问题得到的分数是R2形式 表示x对y的解释程度
    r2_score = model.score(X_test, y_test)
    print(f'模型的R2值：{r2_score}')

    # 单个样本预测
    idx = 50
    single_test_feat = X_test[idx, :]
    y_true = y_test[idx]
    # 必须以列表形式传入样本特征 返回列表形式预测值
    y_pred = model.predict([single_test_feat])[0]
    print('样本特征:', single_test_feat)
    print('真实值：{}，预测值：{}'.format(y_true, y_pred))


if __name__ == '__main__':
    all_data_df = collect_data()
    inspect_data(all_data_df)
    plot_feat_and_price(all_data_df)
    process_and_analyze_data(all_data_df)