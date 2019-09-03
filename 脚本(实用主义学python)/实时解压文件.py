# 指定文件夹内实时按要求解压文件
# 建立一个类 是否是需要保存压缩原文件

import os
import shutil
import time
import threading
import 脚本.CONFIGURE


class ArchiveMonitor:             # 解压文件监视类，以待解压文件夹的不同区分
    def __init__(self, c):
        self.path         = c['path']                                   # 待解压文件路径
        self.path_to_save = c['path_to_save']                           # 压缩包保存路径
        self.scan_time    = int(c['scan_time'])                         # 监测间隔
        self.is_save      = True if c['is_save'] == 'YES' else False    # 是否保存解压包

    def f_to_arch(self, p):            # 扫描待解压文件路径并返回压缩包绝对路径列表
        f = []
        for i in os.listdir(p):
            if i.endswith('.zip'):
                f.append(p + i)
        return f

    def run(self):                                                  # 运行方法 解压文件 并根据参数保存压缩包

        def _run():                                                 # 作为需多线程运行的函数（多个对象同时运行）
            while True:
                files = self.f_to_arch(self.path)
                if files:
                    for f1 in files:
                        shutil.unpack_archive(f1, self.path)        # 解压
                        if self.is_save:
                            shutil.move(f1, self.path_to_save)      # 移动压缩包
                        else:
                            os.remove(f1)                           # 删除压缩包
                time.sleep(self.scan_time)                          # 监测间隔

        t = threading.Thread(target=_run)                           # 建立线程对象
        t.daemon = True                                             # 守护线程
        t.start()                                                   # 启动线程


def main():
    monitors = [ArchiveMonitor(c) for c in 脚本.CONFIGURE.configure3]        # 导入参数并实例化对象列表
    for a in monitors:                                                  # 多个对象同时运行
        a.run()


if __name__ == '__main__':
    main()

