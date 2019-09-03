# 爬取特定用户某时段的微博内容（时间 文字 链接）并保存至csv文件
# div.WB_text.W_f14 内容sel
# div.WB_from.S_txt2 时间sel
# div.WB_from.S_txt2 > a:nth-child(1) 链接sel
# div.WB_feed_detail 每一张微博卡片sel
# a.page.next 下一页sel
# https://weibo.com/u/3779609882?is_ori=1&key_word=&start_time=2018-09-01&end_time=2018-09-19&is_search=1&is_searchadv=1#_0  lihuan时间段微博url
# https://weibo.com/?sudaref=www.baidu.com&display=0&retcode=6102 微博登陆页面
# start_browser -> get_infos -> scroll_down -> save_infos -> next_page
# 做成面向对象形式

import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class LoadWeibo:
    def __init__(self, dur):      # dur的格式为 2018-09-01~2018-09-10
        self.duration     = dur
        st_time, end_time = self.duration.split('~')      # 获取时间段并传入baseurl中 模拟了网页的搜索功能 直接作为参数加入请求打开搜索结果页
        self.base_url     = f'https://weibo.com/u/3779609882?is_ori=1&key_word=&start_time={st_time}&end_time={end_time}&is_search=1&is_searchadv=1#_0'
        self.driver       = self._star_browser()      # 实例化对象即启动浏览器对象

    def _star_browser(self):
        dri = webdriver.Chrome(executable_path='C:\\Users\\shine小小昱\\Desktop\\chromedriver.exe')
        dri.start_client()
        print('已打开浏览器')
        return dri

    def _log_in(self):
        log_in_url = 'https://weibo.com/?sudaref=www.baidu.com&display=0&retcode=6102'   # 微博登陆页
        self.driver.get(log_in_url)
        input('请手动登陆微博后继续')    # 取巧方法 只有等到手动登陆完毕后手动点击才能继续运行程序
        time.sleep(5)

    def _scroll_down(self):
        html_page = self.driver.find_element_by_tag_name('html')   # tag是html语言里<>里面的内容 这里是获取整个html页面对象
        for i in range(15):
            html_page.send_keys(Keys.END)    # 暴力按END键到达底端
            time.sleep(0.8)

    def get_infos(self, base_url):
        self.driver.get(base_url)
        self._scroll_down()
        time.sleep(5)
        info_list   = []
        sel_cards   = 'div.WB_feed_detail'                      # 微博卡片路径
        sel_time    = 'div.WB_from.S_txt2'
        sel_content = 'div.WB_text.W_f14'
        sel_link    = 'div.WB_from.S_txt2 > a:nth-child(1)'

        for card in self.driver.find_elements_by_css_selector(sel_cards):             # 以[[1,2,3],[4,5,6],[7,8,9].....}形式保存
            info_list.append([card.find_element_by_css_selector(sel_time).text,
                              card.find_element_by_css_selector(sel_content).text,
                              card.find_element_by_css_selector(sel_link).get_attribute('href')])

        print('得到原始数据')
        return info_list

    def _save_info(self, list):
        if not os.path.exists(f'/Users/lfish/Desktop/{self.duration}.csv'):
            with open(f'/Users/lfish/Desktop/{self.duration}.csv', 'w+', encoding='utf-8') as f:  # windows打开csv时默认gbk编码 所以要设置参数
                writer = csv.writer(f)
                writer.writerows(list)
            print('已存储数据')
        else:
            with open(f'/Users/lfish/Desktop/{self.duration}.csv', 'a', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(list)
            print('已存储数据')

    def _get_nextpage_url(self):
        sel_nextpage = 'a.page.next'
        if self.driver.find_elements_by_css_selector(sel_nextpage):        # 如果存在下一页的链接 就返回链接
            nextpage_url = self.driver.find_elements_by_css_selector(sel_nextpage)[0].get_attribute('href')
            return nextpage_url

    def run(self):
        self._log_in()
        self._save_info(self.get_infos(self.base_url))
        while self._get_nextpage_url():         # 存在下一页就继续循环操作
            print('存在下一页内容，开始操作....')
            time.sleep(5)
            self._save_info(self.get_infos(self._get_nextpage_url()))  # 并将下一页的url作为新的参数传入
        print(f'{self.duration}期间的微博内容存储完毕！')


if __name__ == '__main__':
    duration = input('请输入要查找的日期范围（例如2018-01-01~2018-03-03）：')
    loading = LoadWeibo(duration)
    loading.run()



