# 用递归方法解决汉诺塔问题

all_columns = 'ABC'  # 所有柱子名称字符串
step_num = 0         # 操作步骤数


def hanoi(strt, dest, num):
    """
    解题函数
    :param strt: 起始柱子名称
    :param dest: 目的柱子名称
    :param num: 汉诺塔层数
    """
    global step_num  # 将step_num全局化以便修改
    passby = all_columns.replace(strt, '').replace(dest, '')  # 得到除起始目的之外的另一根柱子

    if num == 1:    # 汉诺塔层数为1的情况
        print(f'{strt} -> {dest}')
        step_num += 1
        return None

    elif num == 2:  # 汉诺塔层数为2的情况
        print(f'{strt} -> {passby}')
        print(f'{strt} -> {dest}')
        print(f'{passby} -> {dest}')
        step_num += 3
        return None

    else:           # 汉诺塔层数大于2 分解为2的情况递归进行
        hanoi(strt, passby, num-1)
        print(f'{strt} -> {dest}')
        step_num += 1
        hanoi(passby, dest, num-1)


if __name__ == '__main__':
    start       = input('请输入汉诺塔的起始柱子：（A或B或C）')
    number      = int(input('请输入汉诺塔的层数：（大于零的正整数)）'))
    destination = input('请输入需要移动到的目的柱子：（A或B或C)）')
    print('----------------------')
    print('下面是解法：')
    hanoi(start, destination, number)
    print('----------------------')
    print(f'经过{step_num}次移动，汉诺塔已按要求操作完毕！')