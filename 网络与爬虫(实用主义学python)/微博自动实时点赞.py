# 指定用户微博实时点赞
# https://weibo.com/?sudaref=www.baidu.com&display=0&retcode=6102 微博登陆页面
# https://weibo.com/u/3779609882?profile_ftype=1&is_ori=1#_0  lh原创微博界面
# https://weibo.com/lgcloud?profile_ftype=1&is_ori=1#_0 阿拉斯加原创微博界面
# div.WB_feed_handle > div > ul > li:nth-child(4) > a > span > span > span > em.W_ficon.ficon_praised.S_txt2 未点赞的button
# C 还没点赞的按钮
# 手动打开确定人的原创微博主页并持续监测点赞

import time
from selenium import webdriver


def start_browser():   # 打开驱动并启动启动浏览器 返回浏览器对象
    dri = webdriver.Chrome(executable_path='C:\\Users\\shine小小昱\\Desktop\\chromedriver.exe')
    dri.start_client()
    return dri


def give_like():
    weibo_url = 'https://weibo.com/lgcloud?profile_ftype=1&is_ori=1#_0'  # 某用户原创微博地址
    sel       = 'div.WB_feed_handle > div > ul > li:nth-child(4) > a > span > span > span > em.W_ficon.ficon_praised.S_txt2'  # 未点赞的button路径
    driver.get(weibo_url)    # 打开微博登陆页并等待手动登陆
    time.sleep(15)

    buttons = driver.find_elements_by_css_selector(sel)     # 获得当前页面未点赞按钮对象的列表
    if buttons:
        print(f'有{len(buttons)}条微博需要点赞！')
        for button in buttons:
            button.click()
            count = 1
            print(f'点了{count}个赞')
            count += 1
            time.sleep(5)
        print('点赞完毕')
    else:
        print('暂时还没有微博需要点赞')


if __name__ == '__main__':
    login_url = 'https://weibo.com/?sudaref=www.baidu.com&display=0&retcode=6102'
    driver    = start_browser()
    driver.get(login_url)
    time.sleep(30)

    while True:
        give_like()
        time.sleep(600)
