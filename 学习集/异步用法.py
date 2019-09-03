# 当只有一个线程的时候 异步可以解决实现多任务的难题
# 异步模型：当任务A在读写的时候
# 线程就不等它 直接跳出去执行任务B 等到任务A读写完毕后再继续执行任务A 重复动作

import asyncio


async def say_12():   # 在需要执行异步的任务函数前加上async 类似装饰器的效果
    while True:
        print(1)
        r = await asyncio.sleep(1)  # 人工制造堵塞
        print(2)


if __name__ == '__main__':

    # 声明一个loop 是一个可以实现异步的死循环
    loop = asyncio.get_event_loop()
    # 将需要实现异步死循环的任务传入并运行
    loop.run_until_complete(asyncio.wait([say_12(), say_12()]))
    loop.close()

    # 输出结果中 因为函数输出1和输出2直接阻塞了 所以第一次输出1之后
    # 继续下一个任务直至第一个任务脱离堵塞 再把第一个任务执行完毕后执行第二个
