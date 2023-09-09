import math
import re
import random
import time
import datetime
import uuid

import scrapy_redis
from scrapy_redis.spiders import Spider
from scrapy.http.response.html import HtmlResponse
from scrapy.utils.project import get_project_settings
from scrapy.http import JsonRequest

import execjs

import subprocess
from functools import partial  # 这玩意能锁定一个函数的参数

from TuJia.items import TujiaItem

# 锁定subprocess.Popen的encoding参数为"utf-8"
subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")


# class TujiaSpiderSpider(scrapy.Spider):
class TujiaSpiderSpider(scrapy_redis.spiders.Spider):
    name = "Tujia_spider"

    # allowed_domains = ["m.tujia.com"]
    # start_urls = ["https://m.tujia.com/"]

    redis_key = 'spider:start_url'

    def random_L(self, length=8):
        """
        生成一个随机的数字字母大小写 的字符串
        :param length: 长度
        :return: 和长度相等的字符串
        """
        e = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz0123456789'
        list_e = list(e)
        return "".join([random.choice(list_e) for i in range(length)])

    @property
    def pid(self):
        """生成请求参数需要的pid"""
        return self.random_L(28)

    @property
    def jintian(self):
        """生成今天的日期，年-月-日"""
        return str(datetime.datetime.now().strftime("%Y-%m-%d"))  # 2023-3-29

    @property
    def mintian(self):
        """生成明天的日期，年-月-日"""
        return str((datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))  # 2023-3-30

    @property
    def cookie_fas_session_id(self):
        """
        生成请求载荷需要的数据
        :return: _fas_session_id=z4TDmFGJENiSnmekmaewc3De42Sk1680010659306
        """
        setting = get_project_settings()
        js_path = setting.get('JS_PATH')
        with open(js_path, 'r', encoding='utf-8') as f:
            script = f.read()
        ob = execjs.compile(script)
        fas_session_id = ob.call('fas_session_id')  # _fas_session_id=z4TDmFGJENiSnmekmaewc3De42Sk1680010659306
        return fas_session_id

    @property
    def cookie(self):
        """请求需要的返回cookie"""
        dict_cookie = {
            '_fas_uuid': str(uuid.uuid4()) + "-" + str(int(time.time() * 1000)),  # 必须 ,uuid加上时间戳
            'tj_channel_id': 'tujia',
            'clientAgent': 'T_h5',
            'personalRecommend': 'true',
            'tujia.com_MobileContext_StartDate': self.jintian,
            'tujia.com_MobileContext_EndDate': self.mintian,
            '_fas_session_id': self.cookie_fas_session_id.split("=")[1],  # 必须
            "tujia.com_PortalContext_UserToken": '37eb3c84-9d79-4cbe-aebb-cf82f7f521a6',  # 登录账号token
            'tujia.com_PortalContext_UserId': '267315411',  # 账号id
        }
        return dict_cookie

    def join_url(self, url: str, params: dict):
        return url + "?" + '&'.join([f"{k}={v}" for k, v in params.items()])


    def start_requests(self):
        # a=b
        # print(response.text)
        """获取重庆的行政区域之类"""
        # print("1111"*100)
        url = 'https://m.tujia.com/bnbapp-node-h5/h5/search/conditions/fetch'
        params = {
            "pid": self.pid,
            # "refPid": "7jPjN2p0pKtJsmGaRaS7S584y6Pp", #可以是空
            "act": "",
            "_apitsp": str(int(time.time()) * 1000),  # 时间戳
            "_fasTraceId": str(int(time.time() * 1000)) + self.random_L() + '_' + self.pid
        }
        data = {
            "pageIndex": '0',
            "pageSize": '10',
            "conditions": [
                # {
                #     "label": "解放碑/洪崖洞",
                #     "type": 5,
                #     "value": "8_32",
                #     "gType": 2,
                #     "hotRecommend": 'true',
                #     "longitude": 106.5835,
                #     "latitude": 29.563427,
                #     "conditionType": 8,
                #     "redPoint": 'false',
                #     "selectedType": 0,
                #     "isDirectCondition": 'false'
                # },
                {
                    "label": "欢迎度排序",
                    "type": 4,
                    "value": "1",
                    "gType": 4,
                    "hotRecommend": 'false',
                    "longitude": 0,
                    "latitude": 0,
                    "conditionType": -1,
                    "redPoint": 'false',
                    "selectedType": 0,
                    "isDirectCondition": 'false'
                },
                {
                    "label": "重庆",
                    "type": 1,
                    "value": "22",
                    "gType": 0,
                    "hotRecommend": 'false',
                    "longitude": 106.55699920654297,
                    "longitude": 0,
                    "latitude": 29.571300506591797,
                    "latitude": 0,
                    "conditionType": -1,
                    "redPoint": 'false',
                    "selectedType": 0,
                    # "pingYin": "chongqing",
                    # "pinYin": "chongqing",
                    "isDirectCondition": 'false'
                },
                {
                    "label": "离店日期",
                    "type": 3,
                    "value": self.mintian,  # 明天
                    "gType": 0,
                    "hotRecommend": 'false',
                    "longitude": 0,
                    "latitude": 0,
                    "conditionType": -1,
                    "redPoint": 'false',
                    "selectedType": 0,
                    "scope": 0
                },
                {
                    "label": "入住日期",
                    "type": 2,
                    "value": self.jintian,  # 今天
                    "gType": 0,
                    "hotRecommend": 'false',
                    "longitude": 0,
                    "latitude": 0,
                    "conditionType": -1,
                    "redPoint": 'false',
                    "selectedType": 0,
                    "scope": 0
                }
            ],
            "returnFilterConditions": 'true',
            "returnGeoConditions": 'true',
            "specialKeyType": 0,
            "returnNavigations": 'true',
            "excludeUnitIdSet": [],
            "isGetFilterTips": 'false',
            "urlCode": 'null'
        }

        url = self.join_url(url, params)
        yield JsonRequest(url=url, method='POST', data=data, cookies=self.cookie, callback=self.parse)

    def parse(self, response: HtmlResponse, **kwargs):
        """解析出行政区域，根据每个行政区域发生请求，得到每个区域大概有多少民宿"""
        # print(response.json())
        # 每个行政区具体有多少酒店
        url = 'https://m.tujia.com/bnbapp-node-h5/h5/keyword/keywordsearchsuggest/bnb/v2'
        params = {
            "_apitsp": str(int(time.time()) * 1000),
            "_fasTraceId": str(int(time.time() * 1000)) + self.random_L() + '_' + self.pid
        }
        # 拼接url
        url = self.join_url(url, params)
        # print(url)
        resp = response.json()
        # 获取行政区域
        for quxian in resp['data']['allConditions'][1]['subGroups'][3]['items']:
            data = {
                "cityId": 22,  # 代表重庆市
                # "keyword": "云阳县",
                "keyword": quxian['label'],
                "sourceCode": 702,  # 必须，固定的
                "checkInDate": self.jintian,
                "checkOutDate": self.mintian,
                "currentCity": 'false',
                "forCtripHotel": 'false',
                "typeFilter": 0
            }
            meta = {'label': quxian['label'], 'value': quxian['value']}
            yield JsonRequest(url=url, data=data, cookies=self.cookie, callback=self.parse_xinzhen, method='POST',
                              meta=meta)

    def parse_xinzhen(self, response: HtmlResponse, **kwargs):
        """获取民宿的数量，求出需要请求多少次"""
        resp = response.json()
        # 获取一个区县中有多少民宿
        str_number = resp['data']['suggests'][0]['description']  # "该地约有10651套民宿"
        # 用正则表达式提取数据
        number = int(re.findall(r'\d+', str_number)[0])
        # 每页10个数据，计算页数,向上取整
        page_Index = math.ceil(number / 10)
        url = 'https://m.tujia.com/bnbapp-node-h5/h5/search/v2/searchhouse/bnb'
        params = {
            "pid": self.pid,
            # "refPid": "tJd2b0FjiDyYs68HEwbaxh2reRPX",
            "act": "keyword_search",
            "_apitsp": str(int(time.time()) * 1000),
            "_fasTraceId": str(int(time.time() * 1000)) + self.random_L() + '_' + self.pid
        }
        url = self.join_url(url, params)
        for index in range(0, page_Index):
            data = {
                # "pageIndex": 0,
                "pageIndex": index,  # 第几页
                "pageSize": 10,  # 每页10个数据
                "conditions": [
                    {
                        "type": 1,
                        "value": "22",
                        "pinYin": "chongqing",
                        "label": "重庆",
                        "hotRecommend": 'null'
                    },
                    {
                        "type": 5,
                        "value": response.meta['value'],
                        # "value": "12_10647",
                        "label": response.meta['label'],
                        # "label": "云阳县",
                        "hotRecommend": 'null',
                        "gType": 2,
                        "selected": 'true'
                    },
                    {
                        "type": 2,
                        "value": self.jintian,
                        "hotRecommend": 'null'
                    },
                    {
                        "type": 3,
                        "value": self.mintian,
                        "hotRecommend": 'null'
                    }
                ],
                "returnFilterConditions": 'true',
                "returnGeoConditions": 'true',
                "specialKeyType": 0,
                "returnNavigations": 'true',
                "excludeUnitIdSet": [],
                "isGetFilterTips": 'false',
                "urlCode": 'null',
                "feLog": {
                    "h5_base_log": "{\"checkInDate\":\"%s\",\"checkOutDate\":\"%s\",\"cityId\":\"null\",\"lat\":\"null\",\"lng\":\"null\",\"pname\":\"unitList\",\"refpname\":\"unitList\",\"pid\":\"%s\",\"refPid\":\"tJd2b0FjiDyYs68HEwbaxh2reRPX\",\"positionErrorMsg\":\"用户48小时内拒绝过使用定位\"}" %
                                   (self.jintian, self.mintian, self.pid)
                }
            }
            yield JsonRequest(url=url, data=data, callback=self.parse_data, method='POST', cookies=self.cookie)

    def parse_data(self, response: HtmlResponse, **kwargs):
        resp = response.json()
        for data in resp['data']['items']:
            # print(data)
            item = TujiaItem()
            item['region'] = data['address']  # 地区
            item['hotel_name'] = data['unitName']  # 酒店名称
            item['price'] = str(data['productPrice'])  # 价格
            item['room_type'] = data['unitSummeries'][1]['text']  # 房型
            item['unit_id'] = str(data['unitId'])
            yield item
