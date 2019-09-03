# 统计不同专业背景的员工的平均薪资，并用柱状图显示结果

import pandas as pd
import matplotlib.pyplot as plt

data_info_path = 'C:\\Users\\shine小小昱\\Desktop\\data_employee\\employee_info.csv'
data_edu_path  = 'C:\\Users\\shine小小昱\\Desktop\\data_employee\\employee_edu.csv'
save_path      = 'C:\\Users\\shine小小昱\\Desktop\\'


def collect_data():
    """
    载入csv数据至pandas
    :return: 设备数据df， 使用数据df
    """
    f1      = open(data_info_path, encoding='utf-8')      # 中文文件名或中文路径必须这么打开
    cols    = ['EmployeeNumber', 'MonthlyIncome']
    info_df = pd.read_csv(f1, header=0, usecols=cols)               # 可只读取需要的列

    f2      = open(data_edu_path, encoding='utf-8')  # 中文文件名或中文路径必须这么打开
    edu_df  = pd.read_csv(f2, header=0)  # 可只读取需要的列

    return info_df, edu_df


def inspect_data(info_df, edu_df):
    """
    审查数据
    :param info_df: 员工信息df
    :param edu_df: 员工专业df
    :return:
    """
    print('数据预览：')
    print(info_df.head(10))
    print(edu_df.head(10))

    print('数据基本信息：')
    print(info_df.info())
    print(edu_df.info())

    print('数据内容统计：')
    print(info_df.describe())
    print(edu_df.describe())


def process_data(info_df, edu_df):
    """
    数据处理
    :param info_df: 员工信息df
    :param edu_df: 员工专业df
    :return: 处理后的数据
    """
    # 预防处理空值
    info_df.dropna(inplace=True)
    edu_df.dropna(inplace=True)

    # 联合数据
    merged_df = pd.merge(info_df, edu_df, on='EmployeeNumber', how='inner')

    return merged_df


def analyze_data(proc_df):
    """
    分析数据
    :param proc_df: 处理后的数据
    :return: 已分组求月薪均值后排序的df
    """
    # 分组 求月薪均值 排序
    edu_ic_df = proc_df.groupby('EducationField')['MonthlyIncome'].mean().sort_values(ascending=False)

    return edu_ic_df


def save_and_show(edu_ic_df):
    """
    保存csv，绘制保存图像
    :param edu_ic_df: 已分组求月薪均值后排序的df
    :return:
    """

    # edu_ic_df.to_csv(save_path + '专业与收入对比.csv', header=['mean_income'])

    edu_ic_df.plot(kind='bar', rot=0)  # 设置为零激活横排
    plt.title('Education & Income')
    plt.ylabel('mean income')
    plt.tight_layout()
    plt.savefig(save_path + '专业与收入对比.png')
    plt.show()


if __name__ == '__main__':
    data_info_df, data_edu_df = collect_data()
    inspect_data(data_info_df, data_edu_df)
    proc_data_df = process_data(data_info_df, data_edu_df)
    edu_income_df = analyze_data(proc_data_df)
    save_and_show(edu_income_df)