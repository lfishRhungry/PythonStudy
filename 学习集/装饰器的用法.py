# 装饰器的使用
# 包裹已有函数 使其在原有基础上可以实现新的功能


# 装饰器1 以函数作为参数 代表的是函数所在内存地址
def deco1(func):
    # 编写一个包裹函数 将被包裹函数func用新功能包裹起来
    def wrapper(*args, **kwargs):  # func函数如果需要传入参数 就在wrapper函数中传给它
        print('this is deco1')
        func(*args, **kwargs)
        print('deco1 ended')
    return wrapper


def deco2(func):
    # 编写一个包裹函数 将被包裹函数func用新功能包裹起来
    def wrapper(*args, **kwargs):  # func函数如果需要传入参数 就在wrapper函数中传给它
        print('this is deco2')
        func(*args, **kwargs)
        print('deco2 ended')
    return wrapper


# 实现装饰的方法
@deco1  # 包裹在最外层
@deco2  # 包裹在第二层
def add_machine(a, b, c):
    print(a + b + c)


if __name__ == '__main__':
    add_machine(1, 2, 3)
