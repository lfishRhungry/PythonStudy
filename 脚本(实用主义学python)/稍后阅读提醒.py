# 指定时间段打开存储好的页面

import time
import webbrowser
import threading
import 脚本.CONFIGURE


class URLS:                                                  # 每一个类对象即是多个须在统一时间打开的urls
    def __init__(self, c):                                   # 初始化参数
        self.name      = c['name']
        self.read_time = c['read_time']
        self.urls_path = c['urls_path']                      # url的存放的文本文件
        self.urls      = self.parse_url(self. urls_path)     # 解析出具体url内容的列表

    def run(self):

        def _run():                                      # 需多个持续运行的函数
            while True:
                if self.time_to_read():
                    for i in self.urls:
                        webbrowser.open_new_tab(i)       # 浏览器打开url

        t        = threading.Thread(target=_run)         # 函数添加至线程对象 以便多线程运行
        t.daemon = True                                  # 保护线程设置为true 关闭py时可同时关闭多线程
        t.start()                                        # 线程开始运行

    def parse_url(self, p):                              # 解析对象url存放文件夹的url并返回列表
        us = []

        with open(p, 'r') as f:
            for a in f.read().strip('\n').split('\n'):   # 读取urls文本 两头去回车 整理为列表并加入列表
                us.append(a)

        return us

    def time_to_read(self):                              # 判断是否是打开时间
        now_time = time.ctime().split(' ')[-2][:5]       # 实时调整为格式'00:00'（时分）
        return self.read_time == str(now_time)


def main():
    US = [URLS(c) for c in 脚本.CONFIGURE.configure2]             # 列表解析式批量导入参数并实例化对象

    for u in US:                                                 # 所以对象运行 （多线程）
        u.run()


if __name__  == '__main__':
    main()

