# 建立工作空间对象
# 通过在桌面建立和删除制定文件夹的快捷方式，实现切换桌面的工作空间

import 脚本.CONFIGURE                                  # 引入自建的库
import os


class WorkSpace:                                  # 建立工作空间类
    def __init__(self, c):                        # 构造函数 用来输入起始参数，参数从另外的库字典里引入
        self.name        = c['name']              # 工作空间名称
        self.target_path = c['target_path']       # 希望创建的软连接所在的地方（桌面）
        self.foders      = c['folders']           # 原始文件夹绝对路径（列表）

    def switch(self):                                    # 转换方法
        for f in os.listdir(self.target_path):           # 列出桌面原有的文件夹和文件
            if f.split('_')[-1] == 'wkpl':               # 找到带标记的旧软连接并删除
                os.rmdir(self.target_path + f)

        for f in self.foders:
            folder_name = f.split('\\')[-1] + '_wkpl'                            # 剔出原始文件夹的名称并加标记
            command     = ['MKLINK', '/D', self.target_path + folder_name, f]    # 制作创建软连接的cmd口令 软连接地址和原始文件夹地址
            os.system(' '.join(command))                                         # 组合口令并输入cmd
        # os.startfile('想要双击打开的文件地址')     设置此功能时要修改传入的初始化地址参数和构造函数 多app可以通过列表传入并用for循环打开


workplaces = [WorkSpace(i) for i in 脚本.CONFIGURE.configure1]            # 通过列表解析式输入参数并实例化工作空间（列表）

print('请输入想切换的工作空间：（WORK or PLAY）')
answer = input()

for w in workplaces:                   # 比对对象name属性并调用切换方法
    if w.name == answer:
        w.switch()




