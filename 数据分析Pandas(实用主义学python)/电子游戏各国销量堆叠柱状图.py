# 2005-2017全球销量的top20游戏
# 2005—2017各游戏生产商的销量对比，并用堆叠柱状图可视化

# 空值处理 过滤操作 排序操作 新增列 堆叠柱状图

import pandas as pd
import matplotlib.pyplot as plt

data_path = 'C:\\Users\\shine小小昱\\Desktop\\data_pd\\video_games_sales.csv'
save_path = 'C:\\Users\\shine小小昱\\Desktop\\'


def collect_data():
    """
    载入csv数据至pandas
    :return: 所有数据df
    """
    f = open(data_path, encoding='utf-8')      # 中文文件名或中文路径必须这么打开
    data_df = pd.read_csv(f, header=0)
    return data_df


def inspect_data(data_df):
    """
    审查数据
    :param data_df: 所有数据df
    :return:
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
    :param data_df: 所有数据df
    :return: 处理后的df
    """

    # 处理空值
    cln_data_df = data_df.dropna()

    # 按年份过滤
    cond = (cln_data_df['Year'] >= 2005) & (cln_data_df['Year'] <= 2017)
    fil_data_df = cln_data_df[cond].copy()       # 单纯过滤得到的数据基于源数据，之后有操作的话，可以通过拿到拷贝保护源数据

    # 计算全球销量后加入到df数据中，按字典形式增加新列
    fil_data_df['Global_Sales'] = fil_data_df['NA_Sales'] + fil_data_df['EU_Sales'] \
                                  + fil_data_df['JP_Sales'] + fil_data_df['Other_Sales']

    return fil_data_df


def analyze_data(proc_df):
    """
    数据分析
    :param proc_df: 处理好的df
    :return: 全球销量前二十df， 不同发行商各地区销量之和df
    """

    #                   按global列数据排序                升序           取前二十
    top20_df = proc_df.sort_values(by='Global_Sales', ascending=False).head(20)

    # 取销量大于5百万的数据 按发行商分组得到特殊对象 传入列表对象 批量进行sum取和操作 分组之后发行商一列变成索引
    grouped_df = proc_df[proc_df['Global_Sales'] > 5].groupby('Publisher')
    sales_df = grouped_df[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum()

    return top20_df, sales_df


def save_and_show(top20_df, sales_df):
    """
    保存csv， 绘制保存图片
    :param top20_df: 全球销量前二十df
    :param sales_df: 不同发行商各地区销量之和df
    :return:
    """

    #                                             去除索引
    top20_df.to_csv(save_path + 'top20_games.csv', index=False)
    sales_df.to_csv(save_path + 'sales_results.csv')

    # 画top20柱状图    指定横轴纵轴使用的数据列 再转换为横柱状图    去除图例
    top20_df.plot(kind='barh', x='Name', y='Global_Sales', legend=False)
    plt.xlabel('global sales')   # 柱状图设置完之后再操作时 横纵轴以实际为准
    plt.title('Top 20 Games')
    plt.tight_layout()
    plt.savefig(save_path + 'top20_games.png')
    plt.show()

    # 画堆叠柱状图
    sales_df.plot.bar(stacked=True)
    plt.title('Games Sales Comparison')
    plt.ylabel('sales/million')
    plt.tight_layout()
    plt.savefig(save_path + 'sales_comp.png')
    plt.show()


if __name__ == '__main__':
    all_data_df = collect_data()
    inspect_data(all_data_df)
    proc_data_df = process_data(all_data_df)
    top20_games_df, sales_data_df = analyze_data(proc_data_df)
    save_and_show(top20_games_df, sales_data_df)




