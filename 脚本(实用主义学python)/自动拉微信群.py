# 有陌生人发指定认证消息时自动添加好友 有好友发指定消息时自动拉入群
# 扫描消息池并返回符合条件消息 和添加好友信息 -> 添加好友 加群
# 注意 要先有个群

import wxpy
import time
import sys

ccy = wxpy.Bot()                                # 登陆

try:                                                # 规避未建群的异常并结束程序
    group = ccy.groups().search('测试')[0]          # 找到群聊

except:
    print('此群有异常')
    sys.exit()

pwd1 = '拉我进群'
pwd2 = '加我好友'


def get_msg(pwd):                                            # 找到符合加群的信息对象
    time.sleep(5)                                            # 安全保护
    return [msg for msg in ccy.messages if msg.text == pwd]   # 列表解析式


def get_fren(pwd):                                           # 找到符合加好友的信息对象
    time.sleep(5)                                            # 安全保护
    return [msg for msg in ccy.messages if msg.text == pwd]   # 列表解析式


def add_group(g, u):                                         # 输入群对象和好友对象并拉入群
    try:                                                     # 规避添加异常导致的程序终止
        g.add_members(u, use_invitation=True)                # 加群并发送邀请
        return True
    except:                                                  # 异常则返回none值
        return None


while True:
    new_fren_msg = get_fren(pwd2)
    if new_fren_msg:                                         # 存在有人加好友
        print('有人要加好友')
        for m in new_fren_msg:
            new_user = m.card                                # 指代要加好友的好友对象
            ccy.accept_friend(new_user)                      # 添加好友
            new_user.send('你好啊！')
            ccy.messages.remove(m)                           # 消息池中删除此邀请，防止重复添加
            print('已添加 %s ' % str(new_user.name))
            time.sleep(5)

    msgs = get_msg(pwd1)
    if msgs:                                                 # 存在有人要进群
        print('有人要加群')
        for m in msgs:
            user = m.sender                                  # 指代申请对象
            if add_group(group, user):                       # 加群成功
                print('已添加 %s 入群' % str(user.name))
                ccy.messages.remove(m)
                time.sleep(5)
            else:                                            # 加群失败
                print('添加 %s 入群失败' % str(user.name))
                ccy.messages.remove(m)
                time.sleep(5)
