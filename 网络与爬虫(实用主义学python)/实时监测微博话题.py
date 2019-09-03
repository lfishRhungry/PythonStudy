# 实时监测指定微博话题讨论数据
# https://s.weibo.com/weibo/%2523%25E5%25A5%25A5%25E6%2596%25AF%25E5%258D%25A1%2523&Refer=STopic_box
# #pl_topic_header > div.card-topic-a > div > div.total > span:nth-child(2)

from selenium import webdriver
import time


def start_browser():          # 打开浏览器并打开网页
    dri = webdriver.Chrome(executable_path='C:\\Users\\shine小小昱\\Desktop\\chromedriver.exe')  # chrome驱动所在位置 实例化浏览器对象
    dri.start_client()                                 # 打开浏览器
    url = 'https://s.weibo.com/weibo/%2523%25E5%25A5%25A5%25E6%2596%25AF%25E5%258D%25A1%2523&Refer=STopic_box'
    dri.get(url)                             # 打开目标网页
    return dri              # 返回浏览器对象


def find_info():
    sel = '#pl_topic_header > div.card-topic-a > div > div.total > span:nth-child(2)'     # 数据css路径
    ripe_msg = driver.find_elements_by_css_selector(sel)[0].text                          # 根据路径寻值元素列表并取需求元素转化为文本
    return float(ripe_msg.replace('讨论', '').replace('万', ''))                           # 删选文本的数字部分


while True:
    driver = start_browser()
    time.sleep(12)                # 给浏览器打开时间
    cur_count = find_info()
    tar_count = 370
    if cur_count > tar_count:
        print(f'您关注的话题讨论数已经达到{cur_count}万')
        driver.close()
        break
    driver.close()                 # 注意关闭浏览器
    time.sleep(1200)






