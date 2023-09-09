# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/3/17 22:01
# File : run_validate.py

import time
import json
import requests


import subprocess
from functools import partial  # 这玩意能锁定一个函数的参数

# 锁定subprocess.Popen的encoding参数为"utf-8"
subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs
import ddddocr

from huanyuan_png import parse_bg_captcha
from guiji import get_slide_track

session = requests.session()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}


def url1_gt_challenge(url: str, params: dict) -> tuple:
    """
    第一次请求，获取gt和callback
    :param url: 请求地址
    :param params: 请求参数t,是一个时间戳
    :return: gt和challenge
    """
    resp = session.get(url=url, headers=headers, params=params)
    data_json = resp.json()
    return data_json['gt'], data_json['challenge']


def url2_(url, params):
    resp = session.get(url, params=params, headers=headers)
    return resp


def parse_jsonp(jsonp: str, callback: str) -> dict:
    jsonp_str: str = jsonp.replace(callback, "")
    json_str: str = jsonp_str.replace(jsonp_str[-1], "").replace(jsonp_str[0], "")
    dcit_data: dict = json.loads(json_str)
    return dcit_data


def url3_(url: str, params: dict) -> tuple:
    resp = session.get(url=url, headers=headers, params=params)

    # c, s = parse_resp3(resp.text, callback=params['callback'])
    dcit_data = parse_jsonp(resp.text, callback=params['callback'])
    c, s = dcit_data["data"]['c'], dcit_data["data"]['s']
    return c, s


def url4_(url: str, params: dict):
    resp = session.get(url, headers=headers, params=params)


def url5_(url: str, params: dict):
    resp = session.get(url, headers=headers, params=params)
    dict_json = parse_jsonp(resp.text, callback=params['callback'])
    # c,s,bg,fullbg=dict_json["c"],dict_json["s"],dict_json["bg"],dict_json["fullbg"]
    return dict_json["c"], dict_json["s"], dict_json["bg"], dict_json["fullbg"], dict_json["static_servers"],dict_json['challenge']

def url6_(url:str,params:dict):
    resp=session.get(url=url,params=params,headers=headers)
    dict_json=parse_jsonp(resp.text,callback=params['callback'])
    return dict_json
def open_w(params_dict:dict):
    """获取w加密"""
    with open("jiyan.js",'r',encoding="utf-8") as f:
        script=f.read()
    obj=execjs.compile(script)
    w=obj.call("get_w",params_dict)
    return w


def image_(url, save_path, path="bg.jpg"):
    resp = session.get(url, headers=headers)

    with open(path, 'wb') as f:
        f.write(resp.content)
    parse_bg_captcha(path, save_path=save_path)


def image_ddddorc(bg_path, fullbg_path):
    slide = ddddocr.DdddOcr(det=False, ocr=False)
    with open(bg_path, 'rb') as f:
        target_bytes = f.read()
    with open(fullbg_path, 'rb') as f:
        background_bytes = f.read()
    res = slide.slide_comparison(target_bytes, background_bytes)
    # 识别成功后的x坐标
    x_target = res['target'][0]
    return x_target


def main():
    """主函数"""
    url1 = 'https://www.geetest.com/demo/gt/register-slide'
    params1 = {'t': str(int(time.time() * 1000))}
    gt, challenge = url1_gt_challenge(url=url1, params=params1)
    # time.sleep(2)
    # url2 = "https://apiv6.geetest.com/gettype.php"
    # callback = "geetest_" + str(int(time.time() * 1000))  # 回调函数的名字，jsonp
    # params2 = {"gt": gt, "callback": callback}
    # resp2 = url2_(url2, params2)

    # url3 = 'https://apiv6.geetest.com/get.php'
    # callback3 = "geetest_" + str(int(time.time() * 1000))
    # params3 = {"gt": gt, "challenge": challenge, "lang": "zh-cn", "pt": "0", "client_type": 'web',
    #            "w": '', #第一次的w可以不要
    #            "callback": callback3}
    #
    # c, s = url3_(url=url3, params=params3)

    url4 = "https://api.geetest.com/ajax.php"
    callback4 = "geetest_" + str(int(time.time() * 1000))
    params4 = {"gt": gt, "challenge": challenge, "lang": "zh-cn", "pt": "0", "client_type": 'web',
               "w": '',#不需要
               "callback": callback4}
    url4_(url4, params4)

    # time.sleep(2)

    url5 = "https://api.geetest.com/get.php"
    callback5 = "geetest_" + str(int(time.time() * 1000))
    params5 = {
        "is_next": "true",
        "type": "slide3",
        "gt": gt,
        "challenge": challenge,
        "lang": "zh-cn",
        "https": "true",
        "protocol": "https://",
        "offline": "false",
        "product": "embed",
        "api_server": "api.geetest.com",
        "isPC": "true",
        "autoReset": "true",
        "width": "100%",
        "callback": callback5
    }
    c, s, bg, fullbg, static_servers,challenge = url5_(url5, params=params5)
    bg_url = "https://" + static_servers[0] + bg
    fullbg_url = "https://" + static_servers[0] + fullbg

    yuan_bg_path = "yuan_bg.png"
    yuan_fullbg_path = "yuan_fullbg.png"
    yuan_bg = image_(bg_url, yuan_bg_path, path="bg.jpg")
    yuan_fullbg = image_(fullbg_url, yuan_fullbg_path, path="fullbg.jpg")
    x = image_ddddorc(bg_path=yuan_bg_path, fullbg_path=yuan_fullbg_path)
    x=x-7
    guiji_list,passtime=get_slide_track(x)

    params_w = {"c": c, "s": s,
                # 滑动轨迹
                # "tt": [[53, 21, 0], [0, -1, 61], [1, -1, 8], [1, 0, 8], [3, 0, 7], [4, 0, 9], [3, 0, 8], [5, 0, 7],
                #        [5, 0, 8], [5, 0, 9], [7, 0, 7], [5, 0, 9], [5, 0, 8], [4, 0, 7], [5, 0, 9], [6, 0, 8],
                #        [3, 0, 8], [4, 0, 7], [2, 0, 9], [3, 0, 8], [2, 0, 8], [2, 0, 7], [2, 0, 9], [2, 0, 7],
                #        [2, 0, 8], [1, 0, 9], [1, 0, 7], [2, 0, 9], [1, 0, 16], [2, 0, 7], [1, 0, 9], [1, 0, 7],
                #        [3, 0, 8], [1, 0, 8], [2, 0, 8], [1, 0, 8], [2, 0, 8], [2, 0, 9], [2, 0, 7], [2, 0, 8],
                #        [2, 0, 9], [3, 0, 7], [2, 0, 9], [2, 0, 7], [2, 0, 8], [2, 0, 9], [1, 0, 7], [2, 0, 8],
                #        [1, 0, 9], [1, 0, 96], [1, 0, 8], [1, 0, 7], [1, 1, 17], [0, 0, 8]],
                "tt":guiji_list,
                "x": x,
                "challenge": challenge,
                "gt": gt,
                "passtime": passtime,  # 滑动的时间，单位毫秒
                }
    w = open_w(params_w)

    # time.sleep(2)

    url6="https://api.geetest.com/ajax.php"
    params6={
    "gt": gt,
    "challenge": challenge,
    "lang": "zh-cn",
    "$_BCe": "0",
    "client_type": "web",
    "w": w,
    "callback": "geetest_1691891526055"
}

    resp6=url6_(url6,params6)
    print(resp6)
    return resp6

if __name__ == '__main__':
    main()
