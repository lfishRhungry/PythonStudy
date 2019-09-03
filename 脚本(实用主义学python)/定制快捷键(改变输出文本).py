# get combo -> parse combo -> do something
# 文本输入时输入指定组合键得到指定输出内容
# 注意！！！只支持英文输入模式 否则出现乱码！！！

import pynput                 # 监测及控制键盘的库
import time
import threading
import CONFIGURE


class ComboListener:                       # 建立具有得到 即时的用户按键s列表 解析出要求的对应快捷键内容
    def __init__(self, c):
        self.dict      = c                 # 配置参数 快捷键及对应内容 也是不同实例化对象的区别之处
        self.cur_combo = []                # 即时按键s列表
        self._containing_combo()           # 维持监听键盘并得到即时按键列表的方法

    def _on_press(self, key):                      # 用来配置pynput.keyboard.Listener 自动传入按键对象
        try:
            self.cur_combo.append(key.char)        # 字母按键的字母str
        except AttributeError:
            self.cur_combo.append(key.name)        # 非字母按键的名字str

    def _clear_combo(self):                  # 及时清除cur_combo 需要被应用为线程
        while True:
            if self.cur_combo:               # 当开始有输入时计时
                time.sleep(0.7)              # 三个按键快捷键 控制在0.7s
                self.cur_combo.clear()

    def _containing_combo(self):                                   # 维持监听键盘并得到即时按键列表的方法
        l = pynput.keyboard.Listener(on_press=self._on_press)      # 作为一个线程 持续为self._on_press输入按键参数key
        l.daemon = True
        l.start()

        t = threading.Thread(target=self._clear_combo)             # 将清除cur_combo方法作为线程启用
        t.daemon = True
        t.start()

    def _get_combo(self):                               # 得到能在self.dict中寻值的字符串形式
        if len(self.cur_combo) >= 3:                    # 配置参数中快捷键都是三下
            return ''.join(self.cur_combo[-3:])         # 取实时按键列表中最后三个并拼接

    def get_content(self):                         # 如果按键符合规定好的快捷键要求 返回对应的其内容
        com = self._get_combo()
        if com in self.dict.keys():
            return self.dict[com]


def write_down(con):                               # 输入内容并调用键盘打印
    for _ in range(3):
        k.press(pynput.keyboard.Key.backspace)     # 打印之前先调用退格键清除快捷键
    k.type(con)


if __name__ == '__main__':

    cl = ComboListener(CONFIGURE.configure4)           # 实例化对象并传入参数
    k  = pynput.keyboard.Controller()                      # 实例化键盘控制参数

    while True:                                            # 执行的快捷键功能
        combo_content = cl.get_content()
        if combo_content:
            write_down(combo_content)