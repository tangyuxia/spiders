# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/3/23 21:47
# File : Cookies.py

import re
import json

import requests
import execjs
import subprocess
from functools import partial  # 这玩意能锁定一个函数的参数

# 锁定subprocess.Popen的encoding参数为"utf-8"
subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")


class Cookie():
    """
    传入公安部主页的url，调用cookie方法返回一个字典格式的cookie
    """

    def __init__(self, url='https://www.mps.gov.cn/n2253534/n2253535/index.html'):
        self.url = url
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58"}
        self.dict_cookies = {}
        self.session = requests.session()

    def cookie1(self):
        resp1 = self.session.get(url=self.url, headers=self.headers)
        # print(resp1.cookies)
        self.dict_cookies['__jsluid_s'] = resp1.cookies.get('__jsluid_s')
        # 去掉多余的，然后执行js
        script = resp1.text.replace("<script>document.cookie=", '').replace("</script>", '').split(";location")[0]
        # __jsl_clearance_s=1679579129.578|-1|d0y5A0C9mFZ439%2F2TEgQHWte984%3D;max-age=3600;path=/
        cookie1 = execjs.eval(script)
        cookie = cookie1.split(";")[0]  # __jsl_clearance_s=1679589637.489|-1|yUvjgp781pN07qT5erpGxqr2414%3D
        self.dict_cookies['__jsl_clearance_s'] = cookie.split("=")[1]
        return cookie.split("=")[1]  # 1679589637.489|-1|yUvjgp781pN07qT5erpGxqr2414%3D

    def cookie2(self):
        # headers[]
        resp = self.session.get(url=self.url, headers=self.headers, cookies=self.dict_cookies)
        html = resp.text
        obj = re.compile(";go\((?P<go>.*?)\)</script>", re.S)
        go_str = obj.search(html).groups('go')[0]
        go_dic = json.loads(go_str)  # 转换成字典类型

        with open('jsl_pojie.js', 'r', encoding='utf-8') as f:
            script = f.read()
        ob = execjs.compile(script)
        cookie_list = ob.call('cookie', go_dic)  # ['1679593091.825|0|Od9fCo1GH5WnKAIEnAP1l4hU0II%3D', 7]
        self.dict_cookies['__jsl_clearance_s'] = cookie_list[0]
        return cookie_list[0]

    def html(self):
        resp = self.session.get(url=self.url, headers=self.headers, cookies=self.dict_cookies)
        print(resp.text)

    @property
    def cookie(self):
        cookie=self.cookie1()
        cookie2=self.cookie2()
        # print(self.dict_cookies)
        return self.dict_cookies


if __name__ == '__main__':
    cookie = Cookie()
    # print(cookie.cookie())
    a=cookie.cookie
    print(a)
