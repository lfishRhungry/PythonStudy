# base_url = https://movie.douban.com/top250?start=0&filter=    每页25个 start参数实现翻页
# movie_cards_sel = //div[@class='article']/ol[@class='grid_view']/li
# name_sel = //div[@class='article']/ol[@class='grid_view']/li/div/div/div/a/span[1]
# number_sel = //div[@class='article']/ol[@class='grid_view']/li/div/div/em
# score_sel = //div/div/span[@class='rating_num']
# actor_sel = //div[@class='info']/div[@class='bd']/p[1]
# get_page -> get_infos -> save
# 得到豆瓣电影top100的电影信息

import os
import csv
import requests
from 分布式爬虫学习 import lxml


def get_tree(url):
    """
    得到解析过的html结构树
    :param url: 需要解析的网页
    :return: html结构树对象
    """
    return lxml.html.fromstring(requests.get(url).text)


def get_infos():
    """
    根据css搜索路径 使用树对象的xpath方法 得到结构化信息
    :return: 结构化信息 [[name, number, score, actor],[name, number, score, actor].....]
    """
    infos = []
    name_sel = '//div[@class=\'article\']/ol[@class=\'grid_view\']/li/div/div/div/a/span[1]/text()'
    number_sel = '//div[@class=\'article\']/ol[@class=\'grid_view\']/li/div/div/em/text()'
    score_sel = '//div/div/span[@class=\'rating_num\']/text()'
    actor_sel = '//div[@class=\'info\']/div[@class=\'bd\']/p[1]/text()'

    for i in range(25):
        name = tree.xpath(name_sel)[i]
        number = tree.xpath(number_sel)[i]
        score = tree.xpath(score_sel)[i]
        actor = tree.xpath(actor_sel)[i]

        infos.append([name, number, score, actor])
    print('得到信息')
    return infos


def save_infos(infos):
    """
    写入csv文件呢
    :param list: 结构化信息 [[name, number, score, actor],[name, number, score, actor].....]
    :return:
    """
    if os.path.exists('C:\\Users\\shine小小昱\\Desktop\\豆瓣电影.csv'):
        with open('C:\\Users\\shine小小昱\\Desktop\\豆瓣电影.csv', 'a', encoding='utf-8', newline='') as f:  # newline参数用来去除Exel显示的空白行问题
            writer = csv.writer(f)
            writer.writerows(infos)
        print(f'已经存储第{i1 + 1}页信息')
        print('-----------------')
    else:
        with open('C:\\Users\\shine小小昱\\Desktop\\豆瓣电影.csv', 'w+', encoding='utf-8', newline='') as f:  # 单独先存入头部 避免newli参数影响
            writer = csv.writer(f)
            writer.writerow(['影片名称', '排名', '评分', '信息'])    # 写入一列时用writerow单数形式
        with open('C:\\Users\\shine小小昱\\Desktop\\豆瓣电影.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(infos)
        print('已存储第1页信息')
        print('-----------------')


if __name__ == '__main__':

    for i1 in range(4):   # 循环抓取排名top100的电影信息
        base_url = f'https://movie.douban.com/top250?start={i1 * 25}&filter='
        tree = get_tree(base_url)
        print(f'已抓取第{i1 + 1}页数据')
        save_infos(get_infos())

    print('全部存储完毕')

