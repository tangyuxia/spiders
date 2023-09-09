# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/4/9 12:08
# File : zhihu.py

import hashlib

from pymongo import MongoClient
import requests

import subprocess
from functools import partial  # 这玩意能锁定一个函数的参数
# 锁定subprocess.Popen的encoding参数为"utf-8"
subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs

from ZhiHu_c_h import ZhiHu_c_h  # 设置x-zse-93和cookie的d_c0


class ZhiHu:
    def __init__(self):
        # 主页的url q参数是“疫情”两个字
        self.index_url = 'https://www.zhihu.com/search?type=content&q=%E7%96%AB%E6%83%85'
        self.api_url = 'https://www.zhihu.com/api/v4/search_v3'
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-ab-pb": "CkYbAD8ARwC0AGkBagF0ATsCzALXAtgCtwPWBFEFiwWMBZ4FMQbrBicHdAh5CGAJ9AlrCr4KcQuHC+AL5QvmC3EMjwzDDPgMEiMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAA==",
            "x-zse-93": "101_3_3.0",
            # 'x-zse-96': '2.0_QSRJXjpGue2kaotknKvLMjulWK2P4ZSsnjv2nxMgdzCtfVON45RH=VZeVoW07qLP'
            'x-zse-96': '2.0_ORs6oerS5ljLX/6KhoxG5QYwP5LJh1b6fG+NZfmkFtNHQnAn3bCXyYL4KCCQK/Vd',
        }
        self.cookie = {'d_c0': 'AKAWLlmFBxaPTjROzNN8ouE390PTuVU1Ma0=|1671241840'}
        self.params = {
            "gk_version": "gz-gaokao",
            "t": "general",
            "q": "疫情",
            "correction": "1",
            "offset": '0',
            "limit": "20",  # 每页20个
            "filter_fields": "",
            "lc_idx": '0',
            "show_all_topics": "0",
            "search_source": "Normal"
        }
        self.number = 5100
        self.id = []
        self.url_set=set()
        self.zvideo_id = []
        self.id0_list = []
        self.id_q_list = []
        self.parse_data_list=[]

        self.conn = MongoClient(host='localhost', port=27017)
        self.db = self.conn['kaohe']
        self.coll = self.db['zhihu']

        self.search_hash_id_list=[]

    def hashlib_md5(self, url: str):
        url_md5=hashlib.md5(url.encode('utf-8')).hexdigest()
        self.url_set.add(url_md5)
        return url_md5

    def set_cookie_headers(self, number_page=0, search_hash_id: str = None):
        """设置cookie"""
        zhihu = ZhiHu_c_h()
        c_h = zhihu.main(number_page=number_page, search_hash_id=search_hash_id)
        self.headers = c_h['headers']
        self.cookie = c_h['cookie']
        return c_h

    def x96_81(self,x_zst_81=None):
        with open("x96.js", "r", encoding='utf-8') as f:
            script = f.read()
        obj = execjs.compile(script)
        x_zse_96 = obj.call('x_zse_96', self.params,self.cookie,x_zst_81)
        return x_zse_96



    def id_url_list1(self, number_page=0, search_hash_id: str = None):
        """
        获取详情页的url，这个url没有参数，get请求
        :param number_page: 第几页
        :param search_hash_id: 从第二页开始需要的参数
        :return: 一个列表，里面装有url和页面的id
        """
        offset = str(number_page) if number_page == 0 else str(number_page * 20)
        self.params['offset'] = offset
        self.params['lc_idx'] = offset
        if number_page!=0:
            print('不等于0')
            del self.params['search_source']
            # del self.params['correction']
            self.params['search_hash_id'] = search_hash_id
            # self.params['search_hash_id'] = '0bd3cc6d8072c3a20d341ebd3ddc90e8'
            self.params['search_source']="Normal"
            self.params['vertical_info'] = "0,0,0,0,0,0,0,0,0,0"
            self.headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
                "x-ab-pb": "CkYbAD8ARwC0AGkBagF0ATsCzALXAtgCtwPWBFEFiwWMBZ4FMQbrBicHdAh5CGAJ9AlrCr4KcQuHC+AL5QvmC3EMjwzDDPgMEiMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAA==",
                "x-zse-93": "101_3_3.0",
                # "x-zse-96": "2.0_QIG158bf6AGi=OP1o2oXBDyp34//uRKXIQmbsk/5PgItG9XCHbp28o///=BvrnkF",
                # "x-zse-96": self.x96_81(),
                "x-zst-81": "3_2.0aR_sn77yn6O92wOB8hPZnQr0EMYxc4f18wNBUgpTQ6nxERFZmXY0-4Lm-h3_tufIwJS8gcxTgJS_AuPZNcXCTwxI78YxEM20s4PGDwN8gGcYAupMWufIeQuK7AFpS6O1vukyQ_R0rRnsyukMGvxBEqeCiRnxEL2ZZrxmDucmqhPXnXFMTAoTF6RhRuLPFMt1lJxm8br0A9p8Tupm6JxmUgoBUBLfarH9fqV1ocXfrHXxei3C1X3GnUSTvLgXZwF_tCHMPcCycX2pU9VKlu2CuqO0wwe1SGHCcqgmoqHBL9tpuCYZdhCq-hCYHhS1-9L_ubLZyUxKC9O8bugKYBCmhuOLjbSsIgL0-hcLk4V_OGpmCqfzWqSf6_S_pCp83vgqyu38Sc31Q0Ss-wFY3GxGXbHG9JSMbCNLhJL_jJcGfGV_fvLOlwCMuCX0qUFO6UVB7wVKpCoL8DS11qcGjCLfZUp0fgc_QXe8fQSC",
            }
            self.headers['x-zse-96']=self.x96_81(x_zst_81=self.headers['x-zst-81'])

        resp = requests.get(url=self.api_url, headers=self.headers, cookies=self.cookie, params=self.params)
        print(resp.request.url)
        print(resp.request.headers)
        self.hashlib_md5(resp.request.url)
        json_data = resp.json()
        print(json_data)
        print('看看错误')

        search_hash_id = json_data['search_action_info']['search_hash_id']
        self.search_hash_id_list.append(search_hash_id)
        dict_json = json_data['data']
        for data in dict_json:
            if data['type'] == 'zvideo':
                zvideo_id = data['object']['zvideo_id']
                id_dict = {'zvideo_id': zvideo_id, 'url': 'https://www.zhihu.com/zvideo/' + zvideo_id}
                self.id.append(id_dict)
                # url='https://www.zhihu.com/zvideo/1491373236248440832'
            elif data['type'] == 'hot_timing' and data['object'].get('content_items'):
                content_items = data['object'].get('content_items')
                for id_dict in content_items:
                    if id_dict['type'] == 'question':
                        id = id_dict['object']['id']
                        # url='https://www.zhihu.com/question/591906420'
                        id_dict = {'id_obj': id, 'url': 'https://www.zhihu.com/question/' + id}
                        self.id.append(id_dict)
                    elif id_dict['type'] == 'answer':
                        break
            elif data['type'] == 'search_result' and data['object'].get('question'):
                id = data['object']['id']
                question_id = data['object']['question']['id']
                # url='https://www.zhihu.com/question/586044685/answer/2916194860'
                id_dict = {'id_q': id, 'question_id': question_id,
                           'url': 'https://www.zhihu.com/question/' + question_id + '/answer/' + id}
                self.id.append(id_dict)
            elif data['type'] == 'search_result' and not data['object'].get('question'):
                id = data['object']['id']
                id_dict = {'id0': id, 'url': 'https://zhuanlan.zhihu.com/p/' + id}
                # url='https://zhuanlan.zhihu.com/p/513108727'
                self.id.append(id_dict)
        return search_hash_id

    def parse(self):
        for data_dict in self.id:
            parmas = {"order_by": "score", "limit": "20", "offset": ""}
            if data_dict.get('zvideo_id'):
                # 有多少评论
                # size = data_dict['paging']['totals']
                url = 'https://www.zhihu.com/api/v4/comment_v5/zvideos/' + data_dict.get('zvideo_id') + '/root_comment'
                self.zvideo_id.append({'url': url, 'parmas': parmas})
            elif data_dict.get('id0'):
                id = data_dict.get('id0')
                url = 'https://www.zhihu.com/api/v4/comment_v5/articles/%s/root_comment' % id
                self.zvideo_id.append({'url': url, 'parmas': parmas})
            elif data_dict.get('id_q'):
                id = data_dict.get('id_q')
                url = 'https://www.zhihu.com/api/v4/comment_v5/answers/%s/root_comment ' % id
                self.zvideo_id.append({'url': url, 'parmas': parmas})

    def parse_list_yield(self):
        zvideo_id_list = (data_dict for data_dict in self.zvideo_id)
        for zvideo_id in zvideo_id_list:
            yield zvideo_id
        id0_list = (data_dict for data_dict in self.id0_list)
        for id0 in id0_list:
            yield id0
        id_q_list = (data_dict for data_dict in self.id_q_list)
        for id_q in id_q_list:
            yield id_q

    def parse_data(self, data_json: dict):
        for data in data_json['data']:
            dict_pinglun = {'pinglin': data['content']}
            if data['child_comment_count'] > 2 and data['resource_type'] =='answer':
                id = data['id']
                url = 'https://www.zhihu.com/api/v4/comment_v5/answers/%s/root_comment?order_by=score&limit=20&offset='% id
                self.parse_data_list.append(url)
                # yield url
            elif data['child_comment_count'] > 2 and data['resource_type'] =='zvideo':
                id = data['id']
                url = 'https://www.zhihu.com/api/v4/comment_v5/comment/%s/child_comment?order_by=ts&limit=20&offset='%id
                self.parse_data_list.append(url)
                # yield url
            self.coll.insert_one(dict_pinglun)
            print('保存一条成功')
        # if str(data_json['paging']['is_end']) == 'true':
        #     return None

        if data_json['paging']['is_end']== False:
            url=data_json['paging']['next']  # 下一个url
            self.parse_data_list.append(url)
            # url=data_json['paging']['previous']  # 下一个url
            # self.parse_data_list.append(url)



    def url_data_yield(self):
        for url in self.parse_data_list:
            yield url
    def main(self,number_page=0,search_hash_id_str=None):
        search_hash_id=self.id_url_list1(number_page=number_page,search_hash_id=search_hash_id_str)
        self.parse()
        for url_parmas in self.parse_list_yield():
            url_wanzheng=url_parmas['url']+"?"+'&'.join([f"{k}={v}" for k,v in url_parmas['parmas'].items()])
            if hashlib.md5(url_wanzheng.encode('utf-8')).hexdigest() in self.url_set:
                continue
            else:
                resp = requests.get(url=url_wanzheng,headers=self.headers,cookies=self.cookie)
                self.hashlib_md5(resp.request.url)
                if int(resp.status_code)==404:
                    print("404了，下面是url====》")
                    print(resp.request.url)
                    continue
                self.parse_data(resp.json())
            for next_url in self.url_data_yield():
                if hashlib.md5(next_url.encode('utf-8')).hexdigest() in self.url_set:
                    continue
                else:
                    resp = requests.get(url=next_url, headers=self.headers, cookies=self.cookie)
                    if int(resp.status_code) == 404:
                        print("404了，下面是url====》")
                        print(resp.request.url)
                        continue
                    # print(resp.text)
                    self.parse_data_list.append(resp.json()['paging']['next'])
                    self.hashlib_md5(resp.request.url)
                    self.parse_data(resp.json())

        return search_hash_id

    def run(self):
        search_hash_id_str = None
        for i in range(0,5):
            print('下一页了')
            search_hash_id=self.main(number_page=i,search_hash_id_str=search_hash_id_str)
            # search_hash_id_str=search_hash_id
            search_hash_id_str=self.search_hash_id_list[i]


if __name__ == '__main__':
    zhihu = ZhiHu()
    # ch = zhihu.id_url_list1()
    # print(ch)
    # zhihu.main()
    zhihu.run()
    # url_md5=zhihu.hashlib_md5('https://www.zhihu.com/api/v4/comment_v5/comment/10104050229/child_comment?limit=20&offset=1648807068_10105914953_0&order_by=ts')
    # print(url_md5)