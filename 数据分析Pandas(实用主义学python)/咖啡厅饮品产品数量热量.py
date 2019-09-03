# 比较咖啡厅菜单各饮品类型的产品数量，平均热量

# csv读写 pandas数据访问 groupby分组操作 pandas绘图

import pandas as pd
import matplotlib.pyplot as plt

data_path = 'C:\\Users\\shine小小昱\\Desktop\\data_pd\\coffee_menu.csv'
save_path = 'C:\\Users\\shine小小昱\\Desktop\\'


def collect_data():
    """
    读入csv数据至dataframe数据类型
    :return: 所有数据的dataframe
    """
    f       = open(data_path, encoding='utf-8')   # 中文文件名或中文路径必须这么打开
    data_df = pd.read_csv(f, header=0)            # 列名采用第一行
    return data_df


def inspect_data(data_df):
    """
    查看数据特征
    :param data_df: 所有数据的dataframe
    :return:
    """
    print('数据一共有{}行，{}列'.format(data_df.shape[0], data_df.shape[1]))

    print('数据预览：')
    print(data_df.head(10))       # 前十行

    print('数据基本信息：')
    print(data_df.info())         # 行列数 索引 每列数据类型和数量

    print('数据统计信息：')
    print(data_df.describe())     # 每列最小最大值平均值中位数等（仅显示可计算类型）


def analyze_data(data_df):
    """
    得到品名， 平均卡路里等
    :param data_df: 所有数据的dataframe
    :return: 品名个数df， 品名卡路里均值df
    """
    bev_ca_col      = data_df['Beverage_category']
    bev_ca_pur_list = bev_ca_col.unique()             # 返回列表

    print('饮品类别：')
    print(bev_ca_pur_list)

    bev_ca_grouped  = data_df.groupby('Beverage_category')  # 根据制定列进行分组
    bev_ca_count    = bev_ca_grouped['Calories'].count()    # df类型数据 输出每个分组下calories元素数量 即每个分组的个数
    bev_ca_mean_cal = bev_ca_grouped['Calories'].mean()     # df类型数据 输出每个分组下calories值的均值


    return bev_ca_count, bev_ca_mean_cal


def save_and_show(bev_ca_count, bev_ca_mean_cal):
    """
    保存csv 绘制并保存图像
    :param bev_ca_count: 品名个数df
    :param bev_ca_mean_cal: 品名卡路里均值df
    :return:
    """
    #   分组操作之后的df索引自动变为分组基于的列 所以现在的df数据只有一列 用header进行列命名
    bev_ca_count.to_csv(save_path + '饮品数量统计.csv', header=['count'])
    bev_ca_mean_cal.to_csv(save_path + '饮品卡路里均值统计.csv', header=['calories'])

    bev_ca_count.plot(kind='barh')     # 横向条状图
    plt.title('Beverage Count')
    plt.xlabel('count')                # 注意横向条状图的xy坐标轴
    plt.tight_layout()
    plt.savefig(save_path + '饮品数量统计.png')
    plt.show()

    bev_ca_mean_cal.plot(kind='barh')
    plt.title('Beverage Calories Mean')
    plt.xlabel('calories')
    plt.tight_layout()
    plt.savefig(save_path + '饮品卡路里统计.png')
    plt.show()


if __name__ == '__main__':
    # plt.rcParams['font.sans-serif']    = ['SimHei']  # 在matplotlib中添加中文字体    添加中文字体有可能导致特殊符号不能显示
    # plt.rcParams['axes.unicode_minus'] = False       # matplotlib显示中文后导致负号异常 以此解决

    all_data_df = collect_data()
    inspect_data(all_data_df)
    beverage_category_count, beverage_category_mean_calories = analyze_data(all_data_df)
    save_and_show(beverage_category_count, beverage_category_mean_calories)
