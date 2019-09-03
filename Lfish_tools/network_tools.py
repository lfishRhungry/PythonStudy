"""
关于网络操作的一些小工具：

    get_Requests(url)：运用requests方法对指定url发出带上user-agent的get请求并返回响应对象

    get_PhantomJS_driver()：得到无头浏览器PhantomJS已经设置好user-agent的浏览器对象

    get_Chrome_driver()：得到已经设置好user-agent的图形化界面Chrome浏览器对象

    get_headless_Chrome_driver()：得到已经设置好user-agent的图形化界面Chrome浏览器对象

    scroll_to_bottom_by_keyboard(dri)：停地调用键盘END按键 使浏览器不停地到达底端 促使页面全部加载完毕

    scroll_to_bottom_by_JS(dri)：不停地对网页调用Javascript命令 使浏览器不停地到达底端 促使页面全部加载完毕

    scroll_down_by_JS(dri)：调用Javascript命令 使浏览器到达已加载完毕的页面的底端

"""

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import requests


def get_Requests(url):
    """
    运用requests方法对指定url发出带上user-agent的get请求并返回响应对象
    :param url: 需要请求的url
    :return: get请求的响应
    """
    header = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    response = requests.get(url, headers=header)

    return response


def get_PhantomJS_driver():
    """
    得到无头浏览器PhantomJS已经设置好user-agent的浏览器对象
    :return: PhantomJS浏览器对象
    """
    # 设置user_agent并实例化phantomJS 不设置请求头user_agent就无法跳转链接
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap['phantomjs.page.settings.userAgent'] = user_agent
    dri = webdriver.PhantomJS(desired_capabilities=dcap)

    return dri


def get_Chrome_driver():
    """
    得到已经设置好user-agent的图形化界面Chrome浏览器对象
    :return: Chrome浏览器对象
    """
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"')
    dri = webdriver.Chrome()

    return dri


def get_headless_Chrome_driver():
    """
    得到已经设置好user-agent的无头模式Chrome浏览器对象
    :return: Chrome浏览器对象
    """
    # 得到selenium中chrome浏览器设置对象
    chrome_options = Options()
    # 添加设置 无头模式
    chrome_options.add_argument('--headless')
    # 添加设置 user-agent
    chrome_options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"')
    dri = webdriver.Chrome(options=chrome_options)

    return dri


def scroll_to_bottom_by_keyboard(dri):
    """
    在需要拖动滚动条到底端才加载的网页 通过不停地调用键盘END按键 使浏览器不停地到达底端 促使页面全部加载完毕
    由于需要多次按键操作 比较费时间
    :param dri: selenium浏览器对象
    """
    html_page = dri.find_element_by_tag_name('html')   # tag是html语言里<>里面的内容 这里是获取整个html页面对象
    for i in range(20):                  # 调节按键次数
        html_page.send_keys(Keys.END)    # 暴力按END键到达底端
        time.sleep(0.8)


def scroll_to_bottom_by_JS(dri):
    """
    在需要拖动滚动条到底端才加载的网页 通过不停地对网页调用Javascript命令 使浏览器不停地到达底端 促使页面全部加载完毕
    由于需要多次按键操作 比较费时间
    :param dri: selenium浏览器对象
    """
    for i in range(20):    # 调节按键次数
        dri.execute_script('window.scrollTo(0, document.body.scrollHeight)')  # JavaScript命令
        time.sleep(0.8)


def scroll_down_by_JS(dri):
    """
    调用Javascript命令 使浏览器到达已加载完毕的页面的底端
    :param dri: selenium浏览器对象
    """
    dri.execute_script('window.scrollTo(0, document.body.scrollHeight)')  # JavaScript命令

