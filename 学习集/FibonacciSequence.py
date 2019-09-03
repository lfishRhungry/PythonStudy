# 故事得从西元1202年说起，
# 话说有一位意大利青年，名叫斐波那契。
# 在他的一部著作中提出了一个有趣的问题：
# 假设一对刚出生的小兔一个月后就能长成大兔，再过一个月就能生下一对小兔，
# 并且此后每个月都生一对小兔，一年内没有发生死亡，
# 问：一对刚出生的兔子，一年内繁殖成多少对兔子?


def get_count(mon):
    """
    结题函数
    :param mon: 几个月之后
    :return: 兔子数目
    """
    if mon == 1:
        return 2
    elif mon == 2:
        return 2
    else:  # 兔子数目等于上个月存在的兔子数目 加上 上上个月存在的兔子数目在这个月生出的兔子数目
        last_mon = get_count(mon-1)
        last_last_mon = get_count(mon-2)
        return last_last_mon + last_mon


if __name__ == '__main__':
    month = int(input('请输入需要求得数目的时间是几个月之后：(大于0的正整数)'))
    print(f'求得{month}月后兔子数目为：')
    print(get_count(month))