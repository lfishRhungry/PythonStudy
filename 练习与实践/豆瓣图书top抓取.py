

# 得到豆瓣读书top图书信息并存储csv

# infos_example:'[日] 黑柳彻子 著 / 赵玉皎 / 南海出版公司 / 2003-1 / 20.00元'

import csv
from Lfish_tools import my_tools
from Lfish_tools import network_tools
from lxml.html import fromstring

file_name = '豆瓣图书top250.csv'
save_path = '/Users/lfish/Desktop/'
base_url  = 'https://book.douban.com/top250?start='

title_sel = './/div[1]/a'              # 取属性 <a href="https://book.douban.com/subject/3239549/" onclick="&quot;moreurl(this,{i:'0'})&quot;" title="夹边沟记事">夹边沟记事</a>
infos_sel = './/p'                     # 取文本 <p class="pl">杨显惠 / 花城出版社 / 2008-09 / 34.00元</p>
score_sel = './/div[2]/span[2]'        # 取文本 <span class="rating_nums">9.2</span>
com_sel   = './/div[2]/span[3]'        # 取文本 <span class="pl">(\n16914人评价\n)</span>
book_sel  = '//table/tbody/tr/td[2]'   # 每一本书全部信息在网页中所在的div路径


def mk_save_csv_file():
    """
    创建存储csv文件并写好开头
    """
    with open(save_path + file_name, 'w+', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'infos', 'score', 'com'])


def get_one_page_data(url):
    """
    得到指定网页源码
    :param url: 网址
    :return: 网页源码
    """
    driver.get(url)
    my_tools.sleep_and_count_time(5)
    pg_data = driver.page_source
    print('已得到网页数据，正在解析...')

    return pg_data


def get_page_books_data(pg_data):
    """
    通过网页源码得到数据并存储
    :param pg_data: 网页源码
    """
    tr         = fromstring(pg_data)
    books_data = tr.xpath(book_sel)

    for book_data in books_data:   # 在元素中获取属性或者文本只能用元素对象的方法
        title = book_data.find(title_sel).attrib.get('title')
        info  = book_data.find(infos_sel).text
        score = book_data.find(score_sel).text
        com   = book_data.find(com_sel).text.strip('(').strip(')').strip().strip('人评价')  # 提前进行数据处理

        save_one_book([title, info, score, com])


def save_one_book(one_book_data_list):
    """
    存储图书信息
    :param one_book_data_list: 一本书的信息（列表格式）
    """
    with open(save_path + file_name, 'a+', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(one_book_data_list)


if __name__ == '__main__':

    driver = network_tools.get_PhantomJS_driver()
    print('已打开PhantomJS')
    mk_save_csv_file()
    print(f'已建立好存储文件，路径为：{save_path + file_name}')

    for pg_count in range(0, 226, 25):
        print(f'开始操作第{int(pg_count / 25 + 1)}/10页...')
        page_data = get_one_page_data(base_url + str(pg_count))
        get_page_books_data(page_data)
        print(f'第{int(pg_count / 25 + 1)}/10页已操作完毕!')
        print('------------------------------------')

    driver.close()
    driver.quit()
    print('全部存储完毕！')
