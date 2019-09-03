# """This program draws a Binary tree with random color
#                  You can input a integer to decide the deep of the tree,
#                  or the program will draw a random one.
#
#                  After drawing, you can input 's' to save.
#                  You can input 'space' to draw again if you are in random mode.
#
#                  Terminology:
#                  deep: deep of the Binary tree."""

import turtle
import random
import argparse
from datetime import datetime
from PIL import Image

save_dir = "/Users/lfish/Desktop/"  # 绘制图片保存的路径


class BinaryTree:
    """
    可以随机或指定参数画二叉树 还能保存画布
    """

    def __init__(self):
        self.__inter_angle = 30  # 树杈夹角
        self.__step = 40  # 每一节树枝长度
        # 实例化画图对象 并配置部分画图参数
        self.tur = turtle.Turtle()
        self.tur.hideturtle()
        self.tur.pensize(2)
        self.tur.speed(10)
        # 移到初始位置
        self.tur.setheading(90)
        self.tur.backward(100)

    def __getReady(self):
        """
        每次重新开始画图前的准备工作
        :return:
        """
        # 每次开始画树之前 重新指定颜色
        self.tur.color(random.random(),
                       random.random(),
                       random.random())
        self.tur.clear()  # 清除画布
        # 调整好初始位置
        self.tur.penup()  # 做动作之前和做动作之后随时抬笔

    def __getRandomDeep(self):
        """
        随机产生一个树的深度值
        """
        return random.randint(1, 7)

    def __onlyDraw(self, d):
        """
        一个二叉树的绘画
        :param d: 指定的树深度
        """

        if d == 0:  # 深度为零时不画
            return

        if d == 1:  # 正直向前的初始状态下画一个树杈，然后返回原来的位置和方向
            self.tur.left(self.__inter_angle / 2)
            self.tur.pendown()
            self.tur.forward(self.__step)
            self.tur.penup()
            self.tur.backward(self.__step)
            self.tur.right(self.__inter_angle)
            self.tur.pendown()
            self.tur.forward(self.__step)
            self.tur.penup()
            self.tur.backward(self.__step)
            self.tur.left(self.__inter_angle / 2)

        if d > 1:  # 深度大于1时
            # 先画左树杈 并到达枝头
            self.tur.left(self.__inter_angle / 2)
            self.tur.pendown()
            self.tur.forward(self.__step)
            self.tur.penup()
            # 递归下一层
            self.__onlyDraw(d - 1)
            # 再画右树杈 并到达枝头
            self.tur.backward(self.__step)
            self.tur.right(self.__inter_angle)
            self.tur.pendown()
            self.tur.forward(self.__step)
            self.tur.penup()
            # 递归下一层
            self.__onlyDraw(d - 1)
            # 回到初始点并恢复方向
            self.tur.backward(self.__step)
            self.tur.left(self.__inter_angle / 2)

    def draw(self, d):
        """
        画一棵指定深度的二叉树
        :param d: 指定深度
        """
        print("start drawing a tree...")
        self.__getReady()
        self.__onlyDraw(d)
        print("Done! You can input 's' to save it.")

    def randomDraw(self):
        """
        画一棵随机深度的二叉树
        """
        print("start drawing a tree")
        self.__getReady()
        self.__onlyDraw(self.__getRandomDeep())
        print("Done! You can input 's' to save it or 'space' to draw again.")

    def saveImg(self):
        """
        保存当前画布为eps和png格式图片
        """
        # 用实时时间构造文件名
        dateStr = (datetime.now()).strftime("%d%b%Y-%H%M%S")
        fileName = "tree-" + dateStr
        print(f"saving drawing to {save_dir}{fileName}.png/eps")
        # 挑一个画图对象 得到Tkinter的canvas对象 并保存为eps格式
        canvas = self.tur.getscreen().getcanvas()
        canvas.postscript(file=save_dir + fileName + ".eps")
        # 再利用pillow将文件格式转换为png并保存
        img = Image.open(save_dir + fileName + ".eps")
        img.save(save_dir + fileName + ".png", "png")
        print("Saving Done!")


def main():
    """
    主函数
    """
    # 配置命令行解析参数
    descStr = """This program draws a Binary tree with random color
                     You can input a integer to decide the deep of the tree,
                     or the program will draw a random one.

                     You can input 's' to save the picture.
                     or you can input 'space' to draw again if you are in random mode.

                     Terminology:
                     deep: deep of the Binary tree."""
    parser = argparse.ArgumentParser(description=descStr)
    # 可选参数 深度
    parser.add_argument("--deep", dest="deep", required=False, type=int,
                        help="input a integer as the deep of tree.")
    args = parser.parse_args()
    # 实例化对象
    drawer = BinaryTree()
    # 监听s键以保存画布
    drawer.tur.getscreen().onkey(drawer.saveImg, "s")

    if args.deep:  # 有参数输入的情况 画一颗指定树
        drawer.tur.getscreen().listen()  # 开始侦听
        drawer.draw(args.deep)
    else:  # 无参数输入的情况  画一棵随机树
        drawer.tur.getscreen().onkey(drawer.randomDraw, "space")  # 侦听space以再画一棵随机树
        drawer.tur.getscreen().listen()  # 开始侦听
        drawer.randomDraw()

    drawer.tur.getscreen().mainloop()  # 维持窗口事件循环


if __name__ == "__main__":
    main()
