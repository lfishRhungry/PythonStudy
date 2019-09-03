# 读取指定csv文档 编辑指定消息 发送至指定联系人

import time
import wxpy
import csv

file_path = input('请输入文件绝对地址：')
# 'C:\\Users\\shine小小昱\\Desktop\\ScriptDay10\\sample.csv'


def read_info(path1):                                # 读取csv文件获得原始信息
    f     = open(path1, 'r', encoding='utf-8-sig')   # 用此方法打开，不会出错
    infos = csv.DictReader(f)                        # 用order dict字典读取
    return [info for info in infos]                  # 用列表解析式做成[{},{},{},{},.....]其中{}为每一个字典


def make_info(raw_info):                             # 将原始信息格式化成需要发送的信息并封装为列表
    t = '{n}.同学，请于{t},到达{a}，参加{s}。'
    return [t.format(n=i['姓名'],
                     t=i['上课时间'],
                     a=i['上课地址'],
                     s=i['课程']
                     ) for i in raw_info]            # 列表解析式


def send_info(ripe_info):                            # 传入信息列表并发送至对应联系人
    bot = wxpy.Bot()                                 # 实例化聊天机器人 及登陆一个账号
    for msg in ripe_info:
        fren_name = msg.split('.')[0]                # 取得名字
        f         = bot.friends().search(fren_name)  # 搜索好友 获得一个列表（有可能不止一个好友）

        if len(f) == 1:                              # 确定只有一个好友时才发送
            f[0].send(msg)
        else:
            print('请核实好友名称：')
            print(fren_name)

        time.sleep(5)                                # 设定休眠时间，避免被封号哈哈哈哈


raw_msg  = read_info(file_path)
ripe_msg = make_info(raw_msg)
send_info(ripe_msg)


