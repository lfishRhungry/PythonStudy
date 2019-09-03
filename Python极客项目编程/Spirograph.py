# """This program draws Spirographs using the Turtle module.
#                  When run with no arguments,this program draws random Spirographs.
#
#                  Terminology:
#                  R: radius of outer circle
#                  r: radius of inner circle
#                  l: ratio of hole distance to r"""

import math
import turtle
import random
import argparse
from PIL import Image
from datetime import datetime

save_dir = "/Users/lfish/Desktop/"  # 绘制图片保存的路径
width, height = 800, 500  # 电脑像素

turtle.Turtle.getscreen().screensize()
class Spiro:
    """
    一次能够画一条曲线
    """

    def __init__(self, xc, yc, col, R, r, l):
        self.tur = turtle.Turtle()  # 每一个类实例都构造一个画图对象 有助于同时绘制多条曲线
        self.tur.getscreen().screensize(0.8, 0.8)  # 设置画布大小
        self.step = 5  # 绘图时每一笔的角度的增量
        self.tur.shape("arrow")  # 设置光标形状
        self.tur.pensize(1)
        self.tur.speed(10)
        self.drawingComplete = False  # 判断是否画完

        self.setparams(xc, yc, col, R, r, l)
        self.restart()

    def setparams(self, xc, yc, col, R, r, l):
        """
        设置参数
        """
        self.xc, self.yc = xc, yc  # 曲线中心坐标
        self.R, self.r = int(R), int(r)  # 大小圆的半径
        self.l, self.k = l, r / float(R)  # 线段PC与之比，r与R之比
        self.period = self.r / math.gcd(self.r, self.R)  # 通过r除以r和R的最大公约数 得到周期圈数
        self.col = col
        self.tur.color(*col)  # 设置颜色 参数为元组解包
        self.a = 0  # 初始角度为零

    def restart(self):
        """
        重启，为重新开始画图或者第一次画图做准备，使光标落在画笔开始的初始位置并落下
        :return:
        """
        self.drawingComplete = False  # 重新设置为未完成
        self.tur.hideturtle()  # 隐藏光标
        self.tur.penup()  # 抬笔
        R, k, l = self.R, self.k, self.l  # 获取相应参数
        # 计算当角度等于0时的坐标 以便回到初始位置
        a = 0.0
        x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
        y = R * ((1 - k) * math.sin(a) + l * k * math.sin((1 - k) * a / k))
        self.tur.setpos(self.xc + x, self.yc + y)
        self.tur.down()  # 落笔并准备画图

    def draw(self):
        """
        画图，运用连续线段绘制完整曲线
        """
        print("start drawing a spirograph...")
        R, k, l = self.R, self.k, self.l  # 获取需要的参数
        for i in range(0, 360 * int(self.period) + 1, self.step):  # 设置实时角度i 调整好周期圈数和线段的步数
            a = math.radians(i)  # 转换为弧度制
            x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
            y = R * ((1 - k) * math.sin(a) + l * k * math.sin((1 - k) * a / k))
            self.tur.setpos(self.xc + x, self.yc + y)  # 移动到相应位置 一切以设置好的中心坐标为基准
        self.tur.hideturtle()  # 绘制完成后隐藏光标
        print("Done! You can put 's' to save the picture.")

    def update(self):
        """
        更新，运用连续线段绘制曲线的方法，每执行一次只绘制构成曲线的一段直线
        """
        if self.drawingComplete:  # 检查是否绘画完毕
            return

        self.a += self.step  # 增加角度
        R, k, l = self.R, self.k, self.l  # 获取需要的参数
        a = math.radians(self.a)  # 转换为弧度制
        # 计算坐标并移动
        x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
        y = R * ((1 - k) * math.sin(a) + l * k * math.sin((1 - k) * a / k))
        self.tur.setpos(self.xc + x, self.yc + y)  # 移动到相应位置 一切以设置好的中心坐标为基准
        # 超过预定的周期后 完成绘画并隐藏光标
        if self.a >= 360 * int(self.period):
            self.drawingComplete = True
            self.tur.hideturtle()

    def saveDrawing(self):
        """
        保存现有的画布
        """
        # 用实时时间构造文件名
        dateStr = (datetime.now()).strftime("%d%b%Y-%H%M%S")
        fileName = "spiro-" + dateStr
        print(f"saving drawing to {save_dir}{fileName}.png/eps")
        # 挑一个画图对象 得到Tkinter的canvas对象 并保存为eps格式
        canvas = self.tur.getscreen().getcanvas()
        canvas.postscript(file=save_dir + fileName + ".eps")
        # 再利用pillow将文件格式转换为png并保存
        img = Image.open(save_dir + fileName + ".eps")
        img.save(save_dir + fileName + ".png", "png")
        print("Saving Done!")

    def clear(self):
        """
        清除本对象已绘制好的图像
        :return:
        """
        self.tur.clear()


class SpiroAnimator:
    """
    可以随机生成定制数量曲线的类
    """

    def __init__(self, N):  # 随机曲线的数量
        # 批量创建Spiro对象并存入数组
        self.spiros = []
        for i in range(N):
            rparams = self.genRandomParams()  # 得到一组随机餐宿
            spiro = Spiro(*rparams)  # 解包随机参数并使用它实例化对象
            self.spiros.append(spiro)  # 填充进列表

    def draw(self):
        """
        画图，完成对指定数目随机曲线的绘制
        :return:
        """
        print("start drawing some spirograph...")
        nComplete = 0  # 记录已经画好的曲线数目 用来判断是否画完所有曲线
        # 遍历所有画图对象 逐个执行单个对象的更新函数 直至所有图像画完
        while (nComplete != len(self.spiros)):
            nComplete = 0  # 每次循环时清零计数器 以免画完一个图形后就开始重复计数
            for spiro in self.spiros:
                spiro.update()
                # 每绘制好一个图 计数器+1
                if spiro.drawingComplete:
                    nComplete += 1
        print("Done!\n You can put 's' to save the picture or put 'space' to restart.")

    def genRandomParams(self):
        """
        随机产生一组绘制曲线需要的参数
        :return: 一组绘制一条曲线的参数
        """
        # 根据窗口大小，利用随机数模块生成一组参数
        R = random.randint(50, min(width, height) // 2)  # 大圆半径
        r = random.randint(10, 9 * R // 10)  # 小圆半径
        l = random.uniform(0.1, 0.9)  # 均匀分布
        # 随机生成曲线中心坐标
        xc = random.randint(-width // 2, width // 2)
        yc = random.randint(-height // 2, height // 2)
        # 随机生成三元组颜色参数
        col = (random.random(),
               random.random(),
               random.random())
        return (xc, yc, col, R, r, l)  # 返回参数

    def restart(self):
        """
        重启，为重新开始画图或者第一次画图做准备
        :return:
        """
        # 遍历所有spiro画图对象并执行操作
        for spiro in self.spiros:
            spiro.clear()  # 清除本对象画的图
            rparams = self.genRandomParams()  # 获取一组随机参数
            spiro.setparams(*rparams)  # 为本对象重新传入参数
            spiro.restart()  # 调用Spiro对象的重启方法  让每一个Spiro对象准备好再次画图
        self.draw()


def main():
    """
    主函数
    配置命令行解析参数方式
    配置部分画图参数
    配置按键侦听及对应函数操作
    判断是画随机曲线 还是利用用户输入的参数画图
    """
    # 通过解析命令行来来输入参数并运行
    descStr = """This program draws Spirographs using the Turtle module. 
                 When run with no arguments,this program draws random Spirographs.
                 
                 Terminology:
                 R: radius of outer circle
                 r: radius of inner circle
                 l: ratio of hole distance to r"""
    parser = argparse.ArgumentParser(description=descStr)  # 生成命令行参数解析对象并传入描述信息
    # 添加期望的参数  “--”代表是可选参数  参数个数    解析后的参数名称   可选参数是否可以省略
    parser.add_argument("--sparams", nargs=3, dest="sparams", required=False,
                        help="The three arguments in sparams: R, r, l.")  # 参数的帮助信心
    args = parser.parse_args()  # 得到解析后参数

    # 判断是画随机曲线 还是利用用户输入的参数画图
    if args.sparams:  # 有参数的情况 就利用spiro类画指定的一条曲线
        params = [float(x) for x in args.sparams]  # 解包参数为列表并转换为浮点数
        # 随机一个颜色三元组
        col = (random.random(),
               random.random(),
               random.random())
        spiro = Spiro(0, 0, col, *params)  # 实例化spiro对象
        # 侦听按键 按下s时 调用spiro对象存储函数方法
        spiro.tur.getscreen().onkey(spiro.saveDrawing, "s")  # 配置按键对应方法
        spiro.tur.getscreen().listen()  # 开始侦听
        # 开始画图
        spiro.draw()
        spiro.tur.getscreen().mainloop()  # 开始窗口时间循环

    else:  # 无参数输入的情况 就利用spiroanimator类画几条随机曲线
        spiroAnim = SpiroAnimator(4)  # 实例化spiroanimator对象 并输入初始参数（要画几个曲线）
        # 增加侦听按键及对应函数
        spiroAnim.spiros[0].tur.getscreen().onkey(spiroAnim.spiros[0].saveDrawing, "s")  # 按下s时 调用存储函数方法
        spiroAnim.spiros[0].tur.getscreen().onkey(spiroAnim.restart, "space")  # 按下空格就重启
        spiroAnim.spiros[0].tur.getscreen().listen()  # 开始侦听
        # 开始画图
        spiroAnim.draw()
        spiroAnim.spiros[0].tur.getscreen().mainloop()  # 开始窗口事件循环


if __name__ == "__main__":
    main()
