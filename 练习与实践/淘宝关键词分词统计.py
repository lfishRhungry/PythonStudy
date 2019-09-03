# 将‘爬取淘宝商品信息’中得到的标题结果进行分词统计 绘制词云 绘制关键词前十五销量条形图 绘制价格直方图
# 运用jieba库分词，pandas库进行数据处理

from pylab import *
import jieba
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def collect_data(path):
    """
    收集数据
    :param path: 已爬取的到的csv数据路径
    :return: 标题列表 所有数据的df对象
    """
    print('开始收集数据...')
    f      = open(path, encoding='utf-8')           # 文件标题中有中文时，需要先打开在载入pandas
    df     = pd.read_csv(f, sep=',', header=0, dtype='str')  # 取第header列作为行标题，没有就None，自命名用names=[]
    titles = df.标题.values.tolist()       # 取dataframe文件‘标题’一列的值（df文件还有索引）转换为列表
    print('已得到原始数据')
    print('-------------')

    return titles, df


def cut_words(titles):
    """
    运用jieba库分词
    :param titles: 标题列表
    :return: 分词完毕的列表 [[..., ..., ...], [..., ..., ...], ......]
    """
    print('开始分词...')
    title_cut = []

    for title in titles:
        title_cut.append(jieba.lcut(title))      # lcut返回分词列表

    return title_cut


def rid_stop_words(title_cut):
    """
    去除停用词
    :param title_cut: 分词完毕的列表 [[..., ..., ...], [..., ..., ...], ......]
    :return: 去除停用词之后的列表 [[..., ..., ...], [..., ..., ...], ......]
    """
    print('去除停用词...')
    title_pure = []

    for title_c in title_cut:
        line_pure = []
        for word in title_c:
            if word not in stop_words:
                line_pure.append(word)
        title_pure.append(line_pure)

    return title_pure


def distinct_words(title_pure):
    """
    去除每个title中的重复词
    :param title_pure: 去除停用词之后的列表 [[..., ..., ...], [..., ..., ...], ......]
    :return: 每一个title分词去除停用词之后的列表 [[..., ..., ...], [..., ..., ...], ......]
    """
    print('去除停用词...')
    title_clean = []

    for line in title_pure:
        line_clean = []
        for word in line:
            if word not in line_clean:
                line_clean.append(word)
        title_clean.append(line_clean)

    return title_clean


def get_all_words(title_clean):
    """
    将传入列表的子列表合并为大列表 并转换为dataframe对象
    :param title_clean: 每一个title分词去除停用词之后的列表 [[..., ..., ...], [..., ..., ...], ......]
    :return: 所有处理过的词汇数据的dataframe对象
    """
    all_words_list = []

    for line in title_clean:
        for word in line:
            all_words_list.append(word)

    df_all = pd.DataFrame({'allwords': all_words_list})              # 转换时设置行命名

    return df_all


def count_words(df_all):
    """
    计算词频
    :param df_all: 所有处理过的词汇数据的dataframe对象
    :return: 词频dataframe对象
    """
    print('计算词频...')
    df_count         = df_all.allwords.value_counts().reset_index()   # allwords标题下数词 allwords变为索引 所以重新设置索引
    df_count.columns = ['word', 'count']                              # 重设列名

    return df_count


def get_cloud_pic(df_count):
    """
    绘制并保存词云
    :param df_count: 词频dataframe对象
    :return:
    """
    print('绘制词云并保存...')
    # 词云背景图片需要先用matplotlib读取
    background_image = plt.imread('C:\\Users\\shine小小昱\\Desktop\\text.png')

    wc = WordCloud(width=500, height=300, mask=background_image, background_color='white',  # prefer那个参数是水平词出现概率
                   font_path='C:\\Users\\shine小小昱\\Desktop\\msyh.ttc', max_font_size=400, min_font_size=40,
                   prefer_horizontal=1).fit_words({i[0]: i[1] for i in df_count.head(100).values})  # 字典形式添加词和频

    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')      # 关闭坐标轴刻度 当载入为matplotlib显示的图像后 会加入刻度 所以需要关闭
    plt.show()
    wc.to_file('C:\\Users\\shine小小昱\\Desktop\\云测.png')


def get_sale(df_count, df_all):
    """
    得到词频前十五的关键词对应的销售量
    :param df_count: 词频dataframe对象
    :param df_all: 所有处理过的词汇数据的dataframe对象
    :return: 词频前十五的关键词对应的销售量列表
    """
    sale_sum = []

    for w in df_count.word[:15]:
        w_sum = []                                 # 每一个词对应的标题s销量列表
        for i, t in enumerate(df_all.标题.values):
            if w in t:
                w_sum.append(int(df_all.销量[i]))   # 得到符合条件标题对应的销量，并进行数据类型转换，加入列表

        sale_sum.append(sum(w_sum))                 # 计算出总销量后加入总列表

    return sale_sum


def show_bar_pic(df_count, sale_sum):
    """
    画出频率前十五关键词及其对应的销量的条形图
    :param df_count: 词频dataframe对象
    :param sale_sum: 词频前十五的关键词对应的销售量列表
    :return:
    """
    plt.figure()
    #                             透明度       柱状图在刻度的哪个位置 还可以设置color填充颜色
    plt.bar(range(15), sale_sum, alpha=0.8, align='center')
    plt.xticks(range(15), df_count.word[:15], rotation=30)
    plt.title('关键词及对应销量')
    plt.ylabel('销量')
    plt.tight_layout()
    plt.legend(loc='best')
    plt.savefig('C:\\Users\\shine小小昱\\Desktop\\销量.png')
    plt.show()


def show_hist_pic(df_all):
    """
    得到所有价格数据， 并绘制保存直方图
    :param df_all: 所有处理过的词汇数据的dataframe对象
    :return:
    """
    value_list = []
    for pri in df_all.价格.values.tolist():   # 提取出的价格数据转换数据类型
        value_list.append(float(pri))

    plt.figure(figsize=(15, 10))
    plt.hist(value_list, range=(50, 300), bins=10)
    plt.title('价格分布直方图')
    plt.xticks(range(50, 301, 25))
    plt.xlabel('价格')
    plt.ylabel('数量')

    plt.tight_layout()
    plt.legend(loc='best')
    plt.savefig('C:\\Users\\shine小小昱\\Desktop\\价格.png')
    plt.show()


if __name__ == '__main__':

    plt.rcParams['font.sans-serif'] = ['SimHei']       # 解决matplotlib中不能显示中文问题 必须先from pylib import *
    plt.rcParams['axes.unicode_minus'] = False  # matplotlib显示中文后导致负号异常 以此解决

    data_path  = 'C:\\Users\\shine小小昱\\Desktop\\taobao_月饼_data.csv'           # 已爬取到的原始数据

    stop_words = ['月饼', '礼品', '口味', '礼盒', '包邮', '【', '】', '送礼',         # 停用词表
                  '大', '中秋节', '中秋月饼', '2', '饼', '蓉', '多', '个', '味',
                  '斤', '送', ' ', '老', '北京', '云南', '网红老', '中秋', '团购',
                  '特产', '酒家', '枚', '高档', '传统', '黄', '8', '10', '顺丰',
                  '月', '老字号', '*', '酥', '皇', '装', '2018', '小', '克',
                  '皇上']

    title_list, df_all_data = collect_data(data_path)
    title_cut_list          = cut_words(title_list)
    title_pure_list         = rid_stop_words(title_cut_list)
    title_clean_list        = distinct_words(title_pure_list)
    df_all_words            = get_all_words(title_clean_list)
    df_count_words          = count_words(df_all_words)
    sale_sum_list           = get_sale(df_count_words, df_all_data)

    get_cloud_pic(df_count_words)                # 绘制保存云图
    show_bar_pic(df_count_words, sale_sum_list)  # 绘制保存关键词销量条形图
    show_hist_pic(df_all_data)                   # 绘制保存价格直方图

    print('==============')
    print('全部操作完毕')
