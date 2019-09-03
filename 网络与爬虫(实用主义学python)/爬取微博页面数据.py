# 爬去微博首页指定内容微博信息 微博网页的元素css路径会改变？
# login_url: https://weibo.com/?sudaref=www.baidu.com&display=0&retcode=6102
# base_url:  http://s.weibo.com/weibo/%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD&xsort=hot&suball=1&timescope=custom:2018-09-19:2018-09-19&Refer=g
# 采用面向过程编程处理
# start_browser -> log_in -> get_base_url -> scroll_dowm -> get_infos -> save -> next_page

import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def start_browser():   # 打开驱动并启动启动浏览器 返回浏览器对象
    dri = webdriver.Chrome(executable_path='C:\\Users\\shine小小昱\\Desktop\\chromedriver.exe')
    dri.start_client()
    print('已打开浏览器')
    return dri


def log_in():
    driver.get(login_url)
    input("请手动登陆微博后继续....")
    print('已登录')


def scroll_down():      # 暴力滚动之页底
    page_html = driver.find_element_by_tag_name('html')
    for i in range(12):
        page_html.send_keys(Keys.END)
        time.sleep(0.8)


def get_infos(url):     # 获取当页信息
    driver.get(url)
    time.sleep(5)
    scroll_down()
    time.sleep(3)
    info_list = []

    weibo_cards_sel = 'div > div.card-feed'                                  # 微博卡片sel
    content_sel     = 'div.content:nth-child(2) > p.txt:nth-child(2)'        # 微博内容sel
    nick_name_sel   = 'div.content > div.info > div:nth-child(2) > a.name'   # 用户名  sel
    link_sel        = 'div.content > p.from > a:nth-child(1)'                # 微博链接sel
    time_sel        = 'div.content > p.from > a:nth-child(1)'                # 发布时间sel
    post_sel        = 'div > div.card-act > ul > li:nth-child(2) > a'        # 转发量  sel
    comment_sel     = 'div > div.card-act > ul > li:nth-child(3) > a'        # 评论数  sel
    like_sel        = 'div > div.card-act > ul > li:nth-child(4) > a > em'   # 点赞数  sel

    cards = driver.find_elements_by_css_selector(weibo_cards_sel)
    for card in cards:
        nick_name = card.find_element_by_css_selector(nick_name_sel).text
        timing    = card.find_element_by_css_selector(time_sel).text
        content   = card.find_element_by_css_selector(content_sel).text
        link      = card.find_element_by_css_selector(link_sel).get_attribute('href')

        if card.find_elements_by_css_selector(post_sel):
            post = card.find_elements_by_css_selector(post_sel)[0].text
        else:
            post = '0'

        if card.find_elements_by_css_selector(comment_sel):
            comment = card.find_elements_by_css_selector(comment_sel)[0].text
        else:
            comment = '0'

        if card.find_elements_by_css_selector(like_sel):
            like = card.find_elements_by_css_selector(like_sel)[0].text
        else:
            like = '0'

        info_list.append([nick_name, timing, content, post, comment, like, link])
    print(f'已得到{len(cards)}条微博原始数据')

    return info_list


def save_infos(list):
    if os.path.exists('C:\\Users\\shine小小昱\\Desktop\\数据测试.csv'):
        with open('C:\\Users\\shine小小昱\\Desktop\\数据测试.csv', 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(list)
        print('再次存储数据')
    else:
        with open('C:\\Users\\shine小小昱\\Desktop\\数据测试.csv', 'w+', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows([['用户名', '时间', '内容', '转发量', '评论数', '点赞数', '微博链接']] + list) # writerows必须是数组里面的数组才可以写成一行
        print('首次存储数据')


def get_nextpage_url():
    nextpage_sel = 'div.m-page > div > a'
    if driver.find_elements_by_css_selector(nextpage_sel):
        return driver.find_elements_by_css_selector(nextpage_sel)[0].get_attribute('href')


if __name__ == '__main__':
    login_url = 'https://weibo.com/?sudaref=www.baidu.com&display=0&retcode=6102'
    base_url = 'http://s.weibo.com/weibo/%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD&xsort=hot&suball=1&timescope=custom:2018-09-19:2018-09-19&Refer=g'

    driver = start_browser()
    log_in()
    save_infos(get_infos(base_url))

    while get_nextpage_url():
        print('存在下一页数据')
        save_infos(get_infos(get_nextpage_url()))

    print('所有微博数据存储完毕')