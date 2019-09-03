# 运用pymongo库操纵使用MonbgoDB数据库 新建、写入和读取数据


# C:\\Users\\shine小小昱\\Desktop\\Plan-for-combating-master\\week2\\2_1\\2_1code_of_video\\walden.txt

import pymongo

# 链接数据库客户端
client = pymongo.MongoClient('localhost', 27017)
# 创建新的数据库文件
walden = client['walden']
# 数据库文件中创建新的表
sheet_tab = walden['sheet_tab']

path = '/Users/lfish/Desktop/Plan-for-combating-master/week2/2_1/2_1code_of_video/walden.txt'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

    for index, line in enumerate(lines):
        # 构造字典形式单个数据
        data = {
            'index': index,
            'line' : line,
            'words': len(line.split(' '))  # 数有多少个词
        }
        # 表格中插入数据
        sheet_tab.insert_one(data)

# 查询或打印时使用find方法得到所有数据(列表形式) ()可放入筛选条件 筛选条件为字典形式
# $lt/$lte/$gt/$gte/$ne，依次等价于</<=/>/>=/!=。（l表示less g表示greater e表示equal n表示not  ）
for item in sheet_tab.find({'words': {'$gt': 1}}):
    #    可打印单独数据的某一个值 通过列表内key筛选
    print(item['line'])
