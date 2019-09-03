# 爬取指定关键词在淘宝商品搜索结果中的信息并存储，可指定爬取页数
# 运用模拟浏览器webdriver实现操作
# start_drive -> get_data -> save_data

# xpath路径
# title_sel = '//div/div/a[@class=\'J_ClickStat\']/text()'
# price_sel = '//div/div/strong/text()'
# sale_sel = '//div/div/div[@class=\'deal-cnt\']/text()'
# location_sel = '//div/div[@class=\'location\']/text()'

# css路径
# title_sel    = 'div.row.row-2.title > a'
# price_sel    = 'div.price.g_price.g_price-highlight > strong'
# sale_sel     = 'div.deal-cnt'
# location_sel = 'div.location:nth-child(2)'

# base_url = f'https://s.taobao.com/search?q={搜索关键词}&s={44 * （页码减1）}'

import os
import csv
import time
from selenium import webdriver


def star_browser():
    """
    打开chrome浏览器
    :return: 浏览器驱动对象
    """
    dri = webdriver.Chrome(executable_path='C:\\Users\\shine小小昱\\Desktop\\chromedriver.exe')
    dri.start_client()
    print('已打开浏览器\n')
    return dri


def get_elements_text(sel):
    """
    根据搜索路径，返回在浏览器中获取的相应元素的文本信息列表
    :param sel: css搜索路径
    :return: 相应元素的文本信息列表
    """
    text_list     = []
    elem_projects = driver.find_elements_by_css_selector(sel)

    for elem_project in elem_projects:
        text_list.append(elem_project.text)

    return text_list


def save_data(titles, prices, sales, locations):
    """
    保存数据至csv
    :param titles: 标题文本列表
    :param prices: 价格文本列表
    :param sales: 销售量文本列表
    :param locations: 产地文本列表
    :return:
    """
    if os.path.exists(save_path):
        with open(save_path, 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            for t, p, s, l in zip(titles, prices, sales, locations):
                writer.writerow([t, p, s.replace('人付款', ''), l])
    else:
        with open(save_path, 'w+', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['标题', '价格', '销量', '产地'])
            for t, p, s, l in zip(titles, prices, sales, locations):
                writer.writerow([t, p, s.replace('人付款', ''), l])


if __name__ == '__main__':

    depth        = 20                       # 预计爬取的页数
    key_word     = '月饼'                   # 指定的关键词
    title_sel    = 'div.row.row-2.title > a'
    price_sel    = 'div.price.g_price.g_price-highlight > strong'
    sale_sel     = 'div.deal-cnt'
    location_sel = 'div.location:nth-child(2)'
    save_path    = f'C:\\Users\\shine小小昱\\Desktop\\taobao_{key_word}_data.csv'   # 数据存储路径

    print(f'本次爬取商品关键词：{key_word}')
    print(f'预计爬取{depth}页信息')
    print('=====================')

    driver = star_browser()
    for i in range(depth):
        base_url = f'https://s.taobao.com/search?q={key_word}&s={44 * i}'
        driver.get(base_url)
        print(f'正在操作第{i + 1}/{depth}页...')
        time.sleep(6)
        # 采用css搜索路径
        title_list    = get_elements_text(title_sel)
        price_list    = get_elements_text(price_sel)
        sale_list     = get_elements_text(sale_sel)
        location_list = get_elements_text(location_sel)

        print(f'已得到第{i + 1}/{depth}页数据，正在存储...')
        save_data(title_list, price_list, sale_list, location_list)
        print(f'第{i + 1}/{depth}页数据存储完毕')
        print('---------------')
        time.sleep(2)

    print('全部数据存储完毕')

