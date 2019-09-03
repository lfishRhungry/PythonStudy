# 通过api监测指定GitHub用户信息
# https://github.com/kennethreitz
# https://api.github.com/users/kennethreitz/starred

import requests
import time
import webbrowser

api = 'https://api.github.com/users/kennethreitz/starred'   # api地址
info = requests.get(api).json()
last_star = [i['id'] for i in info]                         # 预先设定最后一次star的id信息

while True:
    info = requests.get(api).json()                         # 每次循环重新获取api并对比id 没有的打开对应网址

    for a in info:
        if a['id'] not in last_star:
            webbrowser.open_new_tab(a['html_url'])
    last_star = [i['id'] for i in info]

    time.sleep(600)

