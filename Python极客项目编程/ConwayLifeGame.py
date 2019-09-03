import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 配置全局参数
ON = 255  # 细胞on状态代表的灰度值
OFF = 0  # 细胞off状态代表的灰度值
save_path = "Users/lfish/Desktop/"  # 动画保存路径
# 初始图案参数
glider = np.array([[0, 0, 255],
                   [255, 0, 255],
                   [0, 255, 255]])
bread = np.array([[0, 255, 255, 0],
                  [255, 0, 0, 255],
                  [0, 255, 0, 255],
                  [0, 0, 255, 0]])
vibrator8 = np.array([[255] * 18])
vibrator10 = np.array([[255] * 10])
vibrator33 = np.array([[255] * 33])
vibrator = np.array([[255] * 33])


def randomGrid(N):
    """
    返回一个指定大小的随机像素矩阵
    :param N: 行列数
    :return:
    """
    #                      选择范围    长度   概率列表         变形为方形
    return np.random.choice([ON, OFF], N * N, p=[0.2, 0.8]).reshape(N, N)


def addPattern(i, j, grid, pattern):
    """
    在网格中固定坐标位置更新一个指定图案的像素数组
    :param i: 顶点行索引
    :param j: 顶点列索引
    :param grid: 网格数组
    :param pattern: 指定图案（array数组）
    """
    N = grid.shape[0]  # 获取网格数组大小
    # 通过遍历方式 挨个复制图案至指定坐标的grid像素块中
    for i1 in range(0, pattern.shape[0]):
        for j1 in range(0, pattern.shape[1]):
            # 为了满足边界条件 采用取模方式
            grid[(i + i1) % N, (j + j1) % N] = pattern[i1, j1]


def update(frameNum, img, grid, N):  # 更新函数需要第一个参数为动画帧数
    """
    更新函数：根据此时网格细胞状态 计算下一阶段网格状态 并更新图像和网格数组
    注意！！！更新函数需要第一个参数为动画帧数 尽管可能不会被用到
    :param frameNum:帧数
    :param img: 图像
    :param grid: 网格数组
    :param N: 数组大小
    :return: 更新后的图像
    """
    newGrid = grid.copy()  # 由原网格数组复制 声明一个更新后的网格数组
    # 遍历‘原网格’中的所有像素块
    for i in range(N):
        for j in range(N):
            total = 0  # 声明这个像素块周围的ON状态细胞的数量
            # 通过遍历来求周围所有灰度和 并用取模方式满足边界条件
            for i1 in range(-1, 2):
                for j1 in range(-1, 2):
                    if not (i1 == j1 == 0):
                        total += grid[(i + i1) % N, (j + j1) % N]
            total = int(total / 255)  # ON状态细胞的数量就是灰度和除以ON状态代表的灰度值
            # 根据Conway生命游戏规则来确定新网格数组中本像素块的状态
            if grid[i, j] == ON:  # 原网格中像素块为on模式时
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:  # 原网格中像素块为off模式时
                if total == 3:
                    newGrid[i, j] = ON
    # 更新图像
    img.set_data(newGrid)
    grid[:] = newGrid[:]  # 将原数组更新为新数组
    return img  # 返回图像


def main():
    # 配置命令行接收参数
    descStr = """Runs Conway's Game of Life simulation."""
    parser = argparse.ArgumentParser(description=descStr)
    parser.add_argument("--gridSize", dest="N", required=False)  # 网格数
    parser.add_argument("--movName", dest="movName", required=False)  # 保存的视频文件名称
    parser.add_argument("--interval", dest="interval", required=False)  # 动画更新间隔的毫秒数
    # 增加互斥参数
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--glider", action="store_true", required=False)  # glider图案初始 是否以滑翔机图案开始模拟 声明即为true
    group.add_argument("--bread", action="store_true", required=False)  # bread图案初始
    group.add_argument("--square", action="store_true", required=False)  # square图案初始
    group.add_argument("--vibrator8", action="store_true", required=False)  # vibrator图案初始
    group.add_argument("--vibrator10", action="store_true", required=False)  # vibrator图案初始
    group.add_argument("--vibrator33", action="store_true", required=False)  # vibrator图案初始
    group.add_argument("--vibrator", action="store_true", required=False)  # vibrator图案初始

    # 解析参数
    args = parser.parse_args()

    N = 100  # 默认网格大小
    # N参数存在并符合条件时 设置为用户输入值
    if args.N and int(args.N) > 10:
        N = int(args.N)

    updateInterval = 50  # 默认更新毫秒数
    # updateInterval参数存在时 设置为用户输入值
    if args.interval:
        updateInterval = int(args.interval)

    grid = np.array([])  # 声明网格数组
    # 判断用户是否指定初始图案 并生成相应初始网格数组
    if args.glider:
        grid = np.zeros(N * N).reshape(N, N)  # 生成全零网格数组
        addPattern(1, 1, grid, glider)  # 注入相应图案
    elif args.bread:
        grid = np.zeros(N * N).reshape(N, N)  # 生成全零网格数组
        addPattern(1, 1, grid, bread)  # 注入相应图案
    elif args.vibrator8:
        grid = np.zeros(N * N).reshape(N, N)  # 生成全零网格数组
        addPattern(40, 40, grid, vibrator8)
    elif args.vibrator10:
        grid = np.zeros(N * N).reshape(N, N)  # 生成全零网格数组
        addPattern(40, 40, grid, vibrator10)
    elif args.vibrator33:
        grid = np.zeros(N * N).reshape(N, N)  # 生成全零网格数组
        addPattern(40, 40, grid, vibrator33)
    elif args.vibrator:
        grid = np.zeros(N * N).reshape(N, N)  # 生成全零网格数组
        addPattern(40, 40, grid, vibrator)
    else:
        grid = randomGrid(N)  # 无指定参数情况下 取随机网格素组

    # 配置图像及动画参数
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation="nearest")  # 根据网格数组生成灰度网格
    # 配置动画参数                  图像 更新函数    更新函数需要参数
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N),
                                  frames=10, interval=updateInterval)  # 帧数 和 更新间隔毫秒数
    # movName参数存在时 保存动画至相应地址
    if args.movName:
        ani.save(save_path + args.movName, fps=30, extra_args=["-vcodec", "libx264"])

    plt.show()  # 展示动画


if __name__ == '__main__':
    main()
