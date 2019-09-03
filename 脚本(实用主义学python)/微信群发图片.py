# 群发指定的一张图片至指定微信联系人
# 获取好友姓名 --> 循环发送图片

import wxpy
import time


def get_name():                                      # 获得姓名列表
    n = input('请输入姓名，以空格分开：')
    return n.split(' ')


def send_pic(names, pic_dir):                          # 发送
    ccy = wxpy.Bot()                                   # 登陆

    for n in names:
        n1 = ccy.friends().search(n)

        if len(n1) == 1:
            n1[0].send_image(pic_dir)
            n1[0].send('程序测试，勿回')
        else:
            print('请核查好友 %s ' % n)

        time.sleep(5)


pic_path  = input('请输入图片地址：')
name_list = get_name()
send_pic(name_list, pic_path)
