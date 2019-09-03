# 通过api接口 得到制定GitHub中指定库的信息
# https://api.github.com/search/repositories?q=django
# https://api.github.com/search/repositories?q=topic:django
# 获得的json语言数据一定格式化解析 否则看不清格式

import requests

api     = 'https://api.github.com/search/repositories?q='          # 搜索关键词得到库
eco_api = 'https://api.github.com/search/repositories?q=topic:'    # 搜索关键词得到库相关的topic


def print_info(name):
    info1      = requests.get(api + name).json()
    info2      = requests.get(eco_api + name).json()
    csq_name   = info1['items'][0]['name']                 # 搜索结果中的名字
    star_count = info1['items'][0]['stargazers_count']   # 整型 被star的数量
    fork_count = info1['items'][0]['forks_count']        # 整型
    eco_count  = info2['total_count']                     # 整型 话题相关数

    print('seach name:%s' % name + '\n',
          'consequence name:%s' % csq_name + '\n',
          'star count:%s' % str(star_count) + '\n',
          'fork count:%s' % str(fork_count) + '\n',
          'eco count:%s' % str(eco_count) + '\n',
          '-----------------------------')


names = input('请输入库名称：(空格分开)')
for i in names.split(' '):
    print_info(i)
