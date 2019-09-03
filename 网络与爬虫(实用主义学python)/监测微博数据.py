# 得到指定微博的数据
# https://weibo.com/1323527941/GzArrodP1?type=comment#_rnd1537144552578
# span > span > span > em:nth-child(2)

from selenium import webdriver
import time

url = 'https://weibo.com/1323527941/GzArrodP1?type=comment#_rnd1537144552578'   # 微博地址


def open_browser():
    dri = webdriver.Chrome(executable_path='C:\\Users\\shine小小昱\\Desktop\\chromedriver.exe')   # 实例化chrome驱动
    dri.start_client()                                                                           # 打开
    return dri                                                                                   # 返回对象


def find_info():
    sel = 'span > span > span > em:nth-child(2)'                                                 # css选择路径
    elems = driver.find_elements_by_css_selector(sel)                                            # 用对象方法得到匹配的元素
    return [int(el.text) for el in elems[1:]]                                                    # 取我想要的元素的文本并整型化


driver = open_browser()
driver.get(url)               # 打开网页
time.sleep(12)                # 给予网页下载时间
infos = find_info()
post, com, good = infos
print(f'转发数：{post}')
print(f'评论数：{com}')
print(f'点赞数：{good}')
driver.close()






