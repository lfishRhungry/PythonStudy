# https://www.zhihu.com/signup?next=%2F   登陆界面
# https://www.zhihu.com/ 首页
# div.ContentItem-actions > span > button.Button.VoteButton.VoteButton--up 点赞按钮
# 自动到知乎首页为前五个点赞
# 打开浏览器-> 登陆 -> 点赞

from selenium import webdriver
import time


def start_browser():   # 打开驱动并启动启动浏览器 返回浏览器对象
    dri = webdriver.Chrome(executable_path='C:\\Users\\shine小小昱\\Desktop\\chromedriver.exe')
    dri.start_client()
    return dri


def give_like():       # 已知点赞键的位置 打开首页并点赞前五个
    sel = 'div.ContentItem-actions > span > button.Button.VoteButton.VoteButton--up'
    driver.get(main_url)
    time.sleep(5)
    buttons = driver.find_elements_by_css_selector(sel)[:5]
    for button in buttons:
        button.click()
        time.sleep(3)
    print('点赞成功！')


sign_in_url = 'https://www.zhihu.com/signup?next=%2F'
main_url    = 'https://www.zhihu.com/'
driver      = start_browser()
driver.get(sign_in_url)               # 打开登陆页面并手动登陆
print('成功打开登陆界面，请手动登陆！')
time.sleep(30)
give_like()