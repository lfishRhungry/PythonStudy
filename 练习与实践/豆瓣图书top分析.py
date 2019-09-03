# 对豆瓣图top250信息进行数据分析
# 1、书籍排名 2、作者出现排名 3、各分数段的评论数均值以及价格均值

import pandas as pd
import numpy as np
from Lfish_tools import data_tools
from Lfish_tools import my_tools
import matplotlib.pyplot as plt

save_path = '/Users/lfish/Desktop/'
file_name = '豆瓣图书top250.csv'


def collect_data():
    """
    数据收集
    """
    f  = open(save_path + file_name, encoding='utf-8')
    df = pd.read_csv(f, header=0)
    f.close()

    return df


def process_data(df):
    """
    数据处理：提取价格和作者信息并新增列 将价格信息格式化
    """
    # 从infos列中提取价格新增price列                                  将人民币类型单位数字化
    df['price']  = df['infos'].str.split('/').str.get(-1).str.strip('元').str.strip('CNY ').str.strip(' RMB')  # df对象字符串向量化操作方法
    df['author'] = df['infos'].str.split('/').str.get(0)   # 新增author作者列
    # 遍历price 将非人民币标价的值（即非数字或浮点）设为空值
    for idx in range(df.shape[0]):
        if not my_tools.str_is_number(df.loc[idx, 'price']):
            df.loc[idx, 'price'] = np.nan    # 空值的写法

    return df


def analyze_and_show_data(proc_df):
    """
    分析并作图
    :param proc_df:
    :return:
    """
    # 1、书籍排名                                                   降序排列                 drop将原先索引丢弃（set_index是将某列设为索引）

    df_sort = proc_df[['name', 'score']].sort_values(by='score', ascending=False).reset_index(drop=True)
    df_sort.to_csv(save_path + '书籍排名.csv')


    # 2、作者出现排名

    # 得到作者排名df 得到的df以排名对象为索引 且排名一列没有名字
    df_count = proc_df['author'].value_counts()
    # 过滤数据 取出现次数大1的作者排名 df_count是series 只有一列数据 所以不用指明哪一列
    df_count = df_count[df_count > 1]
    # 设置列名之后保存csv copy数据上操作
    df_count_save = df_count.reset_index()  # 另设置默认索引
    df_count_save.columns = ['作者', '出现次数']   # 设置列名
    df_count_save.to_csv(save_path + '豆瓣读书top作者排名.csv', index=False)  # 保存时不要索引
    # 画图
    df_count.sort_values(inplace=True)   # 为了画出横向柱状图好看 按从小到大排序 源数据上操作
    df_count.plot(kind='barh')
    plt.title('豆瓣读书Top250作者出现次数排名')
    plt.ylabel('作者')    # 注意 横向柱状图声明完毕后 横纵轴参数按实际来设置
    plt.xlabel('出现次数')
    plt.tight_layout()
    plt.savefig(save_path + '作者排名图.png')
    plt.show()


    # 3、各分数段的评论数均值以及价格均值

    #                取需要数据df               按分数升序排列  排列后score变为索引  所以重设索引 不丢弃score
    df_compriscore = proc_df[['com', 'price', 'score']].sort_values(by='score', ascending=True).reset_index(drop=False)
    # 运用cut函数进行分数段分割
    df_compriscore['score'] = pd.cut(df_compriscore['score'],
                                     bins=[-np.inf, 8.2, 8.4, 8.6, 8.8, 9.0, 9.2, 9.4, np.inf],
                                     labels=['8.2以下', '8.2-8.4', '8.4-8.6', '8.6-8.8',
                                             '8.8-9.0', '9.0-9.2', '9.2-9.4', '9.4以上'])
    # 丢掉price的空值 并将其余price转换类型
    df_compriscore.dropna(inplace=True)
    df_compriscore['price'] = df_compriscore['price'].astype('float')
    # 按分段score分组之后 求出各分组的价格评论数均值
    df_compri_mean = df_compriscore.groupby('score')[['com', 'price']].mean()
    # 保存csv文件
    df_compri_mean.to_csv(save_path + '各分数段均价均评论数.csv')

    # 由于均价和评论数数量级相差太大 所以分开作图
    # 评论数均值柱状图
    df_compri_mean['com'].plot(kind='bar', rot=30)
    plt.ylabel('评论数')
    plt.title('各分数段书籍评论数均值')
    plt.savefig(save_path + '各分数段评论数均值.png')
    plt.tight_layout()
    plt.show()
    # 价格均值柱状图
    df_compri_mean['price'].plot()
    # df画折线图时不会默认将索引设置为横轴刻度 需要另行设置
    plt.xticks(range(8),
               ['8.2以下', '8.2-8.4', '8.4-8.6', '8.6-8.8', '8.8-9.0', '9.0-9.2', '9.2-9.4', '9.4以上'],
               rotation=30)
    plt.ylabel('价格')
    plt.title('各分数段书籍价格均值')
    plt.savefig(save_path + '各分数段价格均值.png')
    plt.tight_layout()
    plt.show()




if __name__ == '__main__':

    data_tools.matplotlib_show_CHN()

    data_df = collect_data()
    print('原始数据：')
    data_tools.inspect_df_data(data_df)
    print('----------------------------------------------------')
    proc_data_df = process_data(data_df)
    print('处理好的数据：')
    data_tools.inspect_df_data(proc_data_df)
    print('----------------------------------------------------')
    analyze_and_show_data(proc_data_df)
