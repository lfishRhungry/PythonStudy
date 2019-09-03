# 每日8点左右发送今日军事新闻到手机微信文件助手
# get infos -> make msgs -> send
# https://www.apiopen.top/journalismApi

import wxpy
import requests
import time
from datetime import datetime


def get_infos():
    """
    请求api数据接口得到json数据， 将新闻标题和链接打包为字典
    :return: 字典形式原始信息 {title:link, title:link .......}
    """
    r_datas = {}
    infos   = requests.get(api).json()['data']['war']      # requests get 的信息要解析json

    for r in infos:
        r_datas[r['title']] = r['link']
    return r_datas


def make_msg(r_datas):
    """
    制作需要发送的文本消息
    :param r_datas: 新闻标题和链接打包的字典 {title:link, title:link .......}
    :return: 制作好的待发送消息字符串
    """
    msg = str(datetime.now()).split(' ')[0] + '\nToday\'s tech news :\n'  # 取今日时间
    for i in r_datas.keys():
        msg = msg + i + '\n' + r_datas[i] + '\n\n'
    return msg


if __name__ == '__main__':
    api = 'https://www.apiopen.top/journalismApi'
    ccy = wxpy.Bot()
    tar_hour = 20  # 每日发送的时间 几点

    while True:
        cur_hour = int(str(datetime.now()).split(' ')[1][:2])    # 判断现在时间是否符合
        if cur_hour == tar_hour:   # 符合时间条件才抓起并发送信息
            ripe_data = get_infos()
            messages  = make_msg(ripe_data)
            ccy.file_helper.send_msg(messages)
            time.sleep(82800)           # 休眠23小时
        time.sleep(600)       # 然后每十分钟做一次判断
