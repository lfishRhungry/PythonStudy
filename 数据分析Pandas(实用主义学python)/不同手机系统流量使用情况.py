# 统计不同手机操作系统的每月流量使用情况

# pandas字符串数据处理 pandas数据类型转换 数据联合操作merge

import pandas as pd
import matplotlib.pyplot as plt

data_device_path = 'C:\\Users\\shine小小昱\\Desktop\\data_pd\\mobile_data\\user_device.csv'
data_usage_path  = 'C:\\Users\\shine小小昱\\Desktop\\data_pd\\mobile_data\\user_usage.csv'
save_path        = 'C:\\Users\\shine小小昱\\Desktop\\'


def collect_data():
    """
    载入csv数据至pandas
    :return: 设备数据df， 使用数据df
    """
    f1        = open(data_device_path, encoding='utf-8')      # 中文文件名或中文路径必须这么打开
    device_df = pd.read_csv(f1, header=0)               # 可只读取需要的列

    f2        = open(data_usage_path, encoding='utf-8')  # 中文文件名或中文路径必须这么打开
    usage_df  = pd.read_csv(f2, header=0)  # 可只读取需要的列

    return device_df, usage_df


def inspect_data(device_df, usage_df):
    """
    审查数据
    :param device_df: 设备数据df
    :param usage_df: 使用数据df
    :return:
    """
    print('数据预览：')
    print(device_df.head(10))
    print(usage_df.head(10))

    print('数据基本信息：')
    print(device_df.info())
    print(usage_df.info())

    print('数据内容统计：')
    print(device_df.describe())
    print(usage_df.describe())


def process_data(device_df, usage_df):
    """
    数据处理
    :param device_df: 设备数据df
    :param usage_df: 使用数据df
    :return: 处理完毕的df
    """
    # 字符串列合并
    device_df['platform_version'] = device_df['platform_version'].astype('str')  # 转换数据类型至字符串
    device_df['system'] = device_df['platform'].str.cat(device_df['platform_version'], sep=' ')  # 列字符串合并方法

    # 合并数据集   方法名    带合并数据集          共同基准列   方式（inner,outer,left,right）
    merged_df = pd.merge(device_df, usage_df, on='user_id', how='inner')

    return merged_df


def analyze_data(proc_df):
    """
    数据分析
    :param proc_df: 处理完毕的df
    :return: 按system分组求出月流量均值后已排序的df
    """
    # 以系统分组 计算各分组内月流量使用数据均值 返回df
    sys_mb_df = proc_df.groupby('system')['monthly_mb'].mean()
    # 按值排序（只有一个值，分组后system变为索引） 降序    确定源数据上操作
    sys_mb_df.sort_values(ascending=False, inplace=True)

    return sys_mb_df


def save_and_show(sys_mb_df):
    """
    结果展示
    :param sys_mb_df: 按system分组求出月流量均值后已排序的df
    :return:
    """
    # 结果保存
    sys_mb_df.to_csv(save_path + '手机系统月流量排名.csv', header=['mean_mb'])
    # 绘制柱状图
    sys_mb_df.plot(kind='bar', rot=45)  # 设置横轴刻度旋转角度 横轴默认为索引（system）
    plt.title('System & MB')
    plt.ylabel('Monthly Usage (MB)')
    plt.tight_layout()
    plt.savefig(save_path + '月流量排序.png')
    plt.show()



if __name__ == '__main__':
    data_device_df, data_usage_df = collect_data()
    inspect_data(data_device_df, data_usage_df)
    proc_data_df = process_data(data_device_df, data_usage_df)
    system_mb_df = analyze_data(proc_data_df)
    save_and_show(system_mb_df)

