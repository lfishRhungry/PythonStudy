# 随机生成0到9整数，假设0和1代表遇见badluck，即遇见badluck的概率为20%
# 重复多次试验，注意每次试验的随机性独立，统计每个badluck之间间隔的‘距离’

import numpy as np
import matplotlib.pyplot as plt

s     = ''  # 输出的字符串
wide  = 20000  # 试验次数
count_wide = 50  # 假设每个badluck之间相隔的最大距离
count = [0] * count_wide  # 设置相应列表统计，各个距离出现的次数
data  = np.random.randint(0, 10, wide)  # 生成预定试验次数的随机序列

# 统计各个距离次数
last_ind = 0  # 遍历随机序列，每次循环时最后一次出现0，1的索引位置
for ind, item in enumerate(data):
    if item < 2 and ind != 0:  # 排除序列第一个
        count[ind - last_ind - 1] += 1  # 计数
        last_ind = ind  # 迭代

# 画图
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1)
ax.bar(range(count_wide), np.array(count), alpha=0.7)
ax.plot(range(count_wide), np.array(count), linestyle='-.', c='r', lw=2)
ax.set_xticks(range(0, count_wide))
ax.set_yticks(range(0, 1000, 100))
ax.set_xlim(-1, 50)
ax.set_xlabel('between')
ax.set_ylabel('count')
ax.set_title('why you get bad luck one by one?')

# plt.savefig('/Users/lfish/Desktop/bad_luck.jpg')
plt.show()
