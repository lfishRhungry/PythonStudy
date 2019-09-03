# 通过api实时监测GitHub是否更新 是就打开
# https://api.github.com/repos/channelcat/sanic
# https://github.com/huge-success/sanic
import requests
import time
import webbrowser

api = 'https://api.github.com/repos/channelcat/sanic'      # api 数据接口地址
url = 'https://github.com/huge-success/sanic'              # 网页地址
last_update = None                                         # 上次检查的更新时间先设为无

while True:
    all_info = requests.get(api).json()                    # 获取网页并将json解码
    cur_update = all_info['updated_at']                    # 找到需要的项
    if not last_update:                                    # 如果没有上次更新时间 则将其等于现在查找的更新时间
        last_update = cur_update
    if cur_update > last_update:                           # 比较规范格式的时间大小
        webbrowser.open_new_tab(url)                       # 有更新则打开网页
        last_update = cur_update                           # 更新上次检查的更新时间
    time.sleep(600)