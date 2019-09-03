# 用递归解决阶乘问题

def get_factorial(num):
    """
    求阶乘值的函数
    :param num: 待求值数
    :return: 阶乘结果
    """
    if num == 0:
        return 1
    elif num == 1:
        return 1
    else:
        return num * get_factorial(num-1)


if __name__ == '__main__':
    number = int(input('请输入要计算的递归数字：（大于等于0的正整数)）'))
    print('计算完毕，结果是：')
    print(get_factorial(number))