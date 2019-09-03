# 通过api爬取GitHub指定库的信息
# https://api.github.com/search/repositories?q=language:python

import requests

api     = 'https://api.github.com/search/repositories?q=language:python'  # 搜索只有python语言库的api
url_api = 'https://api.github.com/search/repositories?q='             # 搜索库的api


def get_url(language, size, repo):
    url  = url_api + "language:" + language + "+size:" + size + "+repo:" + repo   # 搜索库的格式
    info = requests.get(url).json()

    if 'items' in info:
        for i in info['items']:
            print(i['html_url'])


def get_name(a):
    all_info = requests.get(a).json()

    for i in all_info['items']:                                                # 符合条件就搜索打印
        if i['created_at'] < '2018-09-16T21:00:06Z' and i['size'] <= 200:
            language = "python"
            size     = "<200"
            repo     = i['html_url'].replace("https://github.com/", "")
            get_url(language, size, repo)


get_name(api)
