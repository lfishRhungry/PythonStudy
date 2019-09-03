# 进程由进程创建 被创建的进程是子进程 每个进程执行自己的任务 互不干扰 进程有属于自己的进程编号 标示着从属关系
# 进程间的内存空间各自独立 比较稳定 消耗内存


from multiprocessing import Process, cpu_count, Queue
import os
import time


# 死循环任务1
def print_A(word, que):
    i = 1
    while True:
        time.sleep(4)
        print(word)
        print(f'正在执行的子进程号：{os.getpid()}')

        print(f'此进程放入Queue一个：{i}')
        que.put(i)
        i += 1
        print(f'此进程放入Queue一个：{i}')
        que.put(i)
        i += 1

        print('---------------------')


# 死循环任务2
def print_B(word, que):
    while True:
        time.sleep(4)
        print(word)
        print(f'正在执行的子进程号：{os.getpid()}')

        print('q队列的size：')
        print(que.qsize())

        i1 = que.get()
        i2 = que.get()
        print(f'此进程取出一个：{i1}')
        print(f'此进程取出一个：{i2}')

        print('---------------------')


# 必须要在声明主函数当中启动进程
if __name__ == '__main__':

    # 父进程创建各进程公用的队列存储对象 并作为参数传入
    q = Queue()

    # 获取cpu内核数目 启动cpu内核数目相等的进程 充分利用计算机资源
    count = cpu_count()
    print(f'当前计算机cpu内核数量为：{count}')
    print(f'主函数进程号：{os.getpid()}')
    print('------------------------------------------------------')


    # 开启两个进程   进程执行的函数   传入参数
    A = Process(target=print_A, args=('A', q))
    B = Process(target=print_B, args=('B', q))

    # 分别启动进程
    # 用A.terminate()结束进程
    A.start()
    # 代表当A进程执行完毕后再继续 timeout参数代表A执行在几秒后还未完成的话 代码继续往下走
    A.join(timeout=2)
    B.start()

