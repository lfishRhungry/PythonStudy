# coding=utf-8
# 线程是真正的执行单位 由进程创建 一个进程当中至少有一个线程
# 多线程效率较高 所以线程共享一个内存空间 出了问题 进程卡死 进程下面所有线程都会瘫痪 python线程不能调用多核cpu
# 进程内的线程之间（包括与父进程之间）数据共享 同属一个内存空间
# 数据虽然能共享 但相互交错的读写同一个变量 很容易造成数据错落

import threading
import time


# 死循环任务1
def print_A(word):
    while True:
        time.sleep(4)

        print('当前线程名：')
        print(threading.current_thread().name)
        print(word)

        # 开始操作共享数据
        lock.acquire()   # 数据上锁后再操作
        global data      # 修改全局变量
        data += 1
        print('已操作共享数据data，并输出：')
        print(data)
        lock.release()   # 数据操作后解锁

        # 创建local()全局字典key并赋值
        l.t1 = 'this t1\'s value of key'
        print(l.t1)

        print('-------------')


# 死循环任务2
def print_B(word):
    while True:
        time.sleep(4)

        print('当前线程名：')
        print(threading.current_thread().name)
        print(word)

        # 开始操作共享数据
        lock.acquire()  # 数据上锁后再操作
        global data     # 修改全局变量
        data += 1
        print('已操作共享数据data，并输出：')
        print(data)
        lock.release()  # 数据操作后解锁

        # 创建local()全局字典key并赋值
        l.t2 = 'this t2\'s value of key'
        print(l.t2)

        print('--------------')


if __name__ == '__main__':

    # local()是一个全局线程可用的字典
    # 各线程内通过赋值变量给不同名字的key 可以相互操作自己的变量互不干扰
    l = threading.local()

    # Lock的机制是一把锁 可以在线程操作数据时将数据锁住防止其他线程操作 直至操作完毕
    lock = threading.Lock()
    data = 0  # 设置被操作数据

    # 定义任务            目标函数          传入参数     定义线程名字
    t1 = threading.Thread(target=print_A, args='A', name='Tread_1')
    t2 = threading.Thread(target=print_B, args='B', name='Tread_2')

    print('主线程名：')
    print(threading.current_thread().name)
    print('--------------------------------------------------------')

    # 启动任务
    # 用t1.terminate()结束进程
    t1.start()
    # 代表当t1线程执行完毕后再继续 timeout参数代表t1执行在几秒后还未完成的话 代码继续往下走
    t1.join(timeout=2)
    t2.start()

