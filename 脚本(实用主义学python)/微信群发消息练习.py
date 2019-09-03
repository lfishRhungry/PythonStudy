# 读取指定csv文档 编辑指定消息 发送至指定联系人
# 获取发送名单 -> 读取csv名单 -> 对比名单并处理发送

import wxpy
import csv


def read_info(path1):                                 # 读取csv文件
    f     = open(path1, 'r', encoding='utf-8-sig')    # 注意编码格式设置
    infos = csv.DictReader(f)
    return [info for info in infos]                   # 列表解析式[{},{},{},........]


def make_msg(r_msg):                                                # 制作具体消息列表
    t = '{n}，提醒下，{t}记得来参加我们的{i}，地点在{d}，{a}。'     # 消息模板
    return [t.format(n=i['微信昵称'],
                     t=i['时间'],
                     i=i['事件'],
                     d=i['地址'],
                     a=i['备注']) for i in r_msg]                   # 格式化 列表解析式


def send_msg(ns, ri_msg):                                           # 判断联系人并发送
    bot = wxpy.Bot()                                                # 登陆

    for n1 in ns:
        count = 0                                                   # 设置触发器 联系人在csv中找到就触发

        for n2 in ri_msg:                                           # 在每一个联系人中再建csv姓名循环并比对
            if n1 == n2.split('，')[0]:
                count = 1                                           # csv中找到 触发
                fre   = bot.friends().search(n1)

                if fre == 1:                                        # 找到唯一好友才发送
                    fre[0].send(n2)
                else:                                               # 否则需手动核查
                    print('请在微信中核查联系人：')
                    print(n1)

        if not count:                                               # 未触发就说明csv中无此人信息
            print('名单中无此人：')
            print(n1)


path      = input('请输入csv路径：')
names     = input('要发给谁：（以空格分开）')
name_list = names.split(' ')
raw_info  = read_info(path)
ripe_msg  = make_msg(raw_info)
send_msg(name_list, ripe_msg)
