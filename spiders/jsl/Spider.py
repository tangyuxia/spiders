# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/3/24 12:27
# File : Spider.py
import time

import requests
from urllib.parse import urljoin
from lxml import etree
from Cookies import Cookie
import pymysql
from pymysql.converters import escape_string


# from pymysql import escape_string


# import Cookies


class GongAn():
    def __init__(self, url='https://www.mps.gov.cn/n2253534/n2253535/index.html'):
        self.page_size = 101  # 爬取100页
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58"}
        self.cookie = {}
        self.page_url_list = None
        self.coon = pymysql.Connection(host='127.0.0.1', port=3306, user='root', password='123456', database='kaohe',
                                       charset='utf8')

    @property
    def set_cookie(self):
        """设置cookie"""
        # 先清空
        self.cookie.clear()
        # 获取cookie
        cookie = Cookie()
        self.cookie = cookie.cookie
        return self.cookie

    def parse1(self, html):
        """
        解析传入的html
        :param html:
        :return:
        """
        h = etree.HTML(html)
        list_href = h.xpath("//ul[@class='list']//a/@href")
        page_href_list = h.xpath('//div[@style="display:none"]/a/@href')
        r = [urljoin(self.url, href) for href in page_href_list]  # 拼接url
        r.reverse()  # 并且倒叙
        self.page_url_list = r,  # 放到这个里面取
        # print(self.page_url_list[0])
        return [urljoin(self.url, href) for href in list_href]

    def parse2(self, html):
        h = etree.HTML(html)
        # title = h.xpath('//meta[@name="ArticleTitle"]/@content')[0]  # 标题
        try:
            title = h.xpath('//title/text()')[0]  # 标题
            Pu_time = h.xpath('//meta[@name="PubDate"]/@content')[0]  # 发布时间
            abstract_list = h.xpath("//div[@class='wordContent w915']/p/text()")  # 摘要
            abstract = ''.join(abstract_list)  # 不去掉空格直接拼接
            data_dcit = {"title": title, 'Pu_time': Pu_time, "abstract": abstract}
            return data_dcit
        except Exception as e:
            print(e)
            print("报错了")
            print(html)
            return None

    def parse_page(self, html):
        """每一页的数据，共10个详情页"""
        h = etree.HTML(html)
        page_number_list = h.xpath('//ul//a/@href')
        return [urljoin(self.url, href) for href in page_number_list]

    def get_text(self, url=None):
        """
        发送get请求
        :param url: 如果url是空，代表第一次请求，用初始化方法里面的url
        :return: html文本
        """
        if url is None:
            url = self.url
        resp = requests.get(url=url, headers=self.headers, cookies=self.cookie)
        resp.encoding = 'utf-8'
        return resp.text

    def mysql_pip(self, data):
        """存入数据库"""
        title = data['title']
        Pu_time = data['Pu_time']
        abstract = data['abstract']
        if '"' in abstract or "'" in abstract:
            # 如果引号在数据里面就转义
            abstract = escape_string(abstract)
        # 创建sql语句
        sql = """insert into gongan(title,Pu_time,abstract) values ("%s","%s","%s")""" % (title, Pu_time, abstract)
        # 创建游标
        sur = self.coon.cursor()
        # 执行sql语句
        sur.execute(sql)
        # 提交
        self.coon.commit()

    def run(self):
        xianzai = time.time()
        index_page = 0
        # 先设置cookie
        cookie = self.set_cookie
        html = self.get_text()
        url_list = self.parse1(html)
        for url in url_list:
            # 首页单独存
            html2 = self.get_text(url)
            data_list = self.parse2(html2)
            if data_list:
                # 存入数据库
                self.mysql_pip(data_list)
                print(data_list)
                # time.sleep(11111)
            else:
                # 如果报错了就跳过
                continue
        for p_url in self.page_url_list[0]:
            xiangqin_html = self.get_text(p_url)
            # 拿到详情页的url，共10个
            index_page += 1
            if index_page > self.page_size:
                # 爬取100页后跳出循环
                break
            url_list_10_page = self.parse_page(xiangqin_html)
            for url in url_list_10_page:
                html2 = self.get_text(url)
                data_list = self.parse2(html2)
                if data_list:
                    # 存入数据库
                    self.mysql_pip(data_list)
                    print(data_list)
                    # time.sleep(11111)
                else:
                    # 如果报错了就跳过
                    continue

            dqtime = time.time()
            if dqtime - xianzai > 30:
                # 30秒刷新一次
                # 抓完10条数据就刷新一下cookie
                shuaxin = self.set_cookie
                xianzai=time.time()
                print(shuaxin)


if __name__ == '__main__':
    gongan = GongAn()
    gongan.run()
