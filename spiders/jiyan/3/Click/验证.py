# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/8/14 7:53
# File : 验证.py
import json
import time
import base64

import requests
import subprocess
from functools import partial  # 这玩意能锁定一个函数的参数

# 锁定subprocess.Popen的encoding参数为"utf-8"
subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs

from yunma import YdmVerify

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}


def get_gt_challenge(url: str, params: dict) -> tuple:
    """"""
    resp = session.get(url=url, params=params, headers=headers)
    resp_json = resp.json()
    gt, challenge = resp_json['gt'], resp_json['challenge']
    return gt, challenge


def parse_jsonp(jsonp: str) -> dict:
    """
    解析jsonp为字典
    :param jsonp: jsonp
    :return: 解析后的数据
    """
    json_str: str = jsonp[jsonp.index("(") + 1:jsonp.rindex(")")]

    return json.loads(json_str)


def request_url2(url: str, params: dict) -> None:
    """
    第3个url的请求
    :param url: url
    :param params: 参数
    :return:
    """
    resp = session.get(url=url, params=params, headers=headers)


def request_url3(url: str, params: dict) -> None:
    """
    第3个url的请求
    :param url: url
    :param params: 参数
    :return:
    """
    resp = session.get(url=url, params=params, headers=headers)


def request_url4(url: str, params: dict) -> None:
    """
    第4个url的请求
    :param url: url
    :param params: 请求参数
    :return:
    """
    resp = session.get(url=url, params=params, headers=headers)


def request_url5(url: str, params: dict) -> tuple:
    """
    第五个url的请求
    :param url: url
    :param params: 参数
    :return: c,s,pic  pic是图片地址
    """
    resp = session.get(url=url, params=params, headers=headers)
    data_dict: dict = parse_jsonp(resp.text)
    pic = data_dict['data']['pic']
    pic_imag = "https://" + data_dict["data"]["image_servers"][0] + data_dict['data']['pic']
    c, s = data_dict['data']['c'], data_dict['data']['s'],
    return c, s, pic, pic_imag


def request_url6(url: str, params: dict) -> dict:
    resp = session.get(url=url, params=params, headers=headers)
    json_dict = parse_jsonp(resp.text)
    return json_dict


def dow_image(url: str, params: dict) -> str:
    """
    下载图片
    :param url: 图片下载地址
    :param params: 参数
    :return: b64编码的字符串
    """
    resp = session.get(url=url, params=params, headers=headers)
    b64_image = base64.b64encode(resp.content).decode("utf-8")
    return b64_image


def cilk_jiyan_a(data: dict[str, str, dict[str, str]]) -> str | None:
    if data.get("code") == 10000:
        return data['data']["data"]
    return None


def open_js_w(params: dict) -> str:
    with open("jiyan.js", 'r', encoding="utf-8") as f:
        script = f.read()
    js = execjs.compile(script)
    w = js.call("get_w", params)
    return w


def main()->dict:
    url1 = "https://www.geetest.com/demo/gt/register-click"
    params1 = {"t": str(int(time.time() * 1000))}
    gt, challenge = get_gt_challenge(url1, params1)

    # time.sleep(1)

    url2 = "https://apiv6.geetest.com/gettype.php"
    params2 = {
        "gt": gt,
        "callback": "geetest_1691970909667"
    }
    request_url2(url2, params2)

    # time.sleep(1)

    url3 = "https://apiv6.geetest.com/get.php"
    params3 = {
        "gt": gt,
        "challenge": challenge,
        "lang": "zh-cn",
        "pt": "0",
        "client_type": "web",
        "w": "",
        "callback": "geetest_" + str(int(time.time() * 1000))
    }
    request_url3(url3, params3)

    time.sleep(1)

    url4 = "https://api.geevisit.com/ajax.php"
    params4 = {
        "gt": gt,
        "challenge": challenge,
        "lang": "zh-cn",
        "pt": "0",
        "client_type": "web",
        "w": "",
        "callback": "geetest_" + str(int(time.time() * 1000))
    }
    request_url4(url4, params4)

    # time.sleep(1)

    url5 = "https://api.geevisit.com/get.php"
    params5 = {
        "is_next": "true",
        "type": "click",
        "gt": gt,
        "challenge": challenge,
        "lang": "zh-cn",
        "https": "true",
        "protocol": "https://",
        "offline": "false",
        "product": "float",
        "api_server": "api.geevisit.com",
        "isPC": "true",
        "autoReset": "true",
        "width": "100%",
        "callback": "geetest_" + str(int(time.time() * 1000))
    }
    # c,s,pic后面w加密需要用到 pic_url是图片下载的地址
    c, s, pic, pic_url = request_url5(url=url5, params=params5)

    image_params = {"challenge": challenge}
    # 下载点选验证码图片,返回b64格式
    b64_image = dow_image(url=pic_url, params=image_params)

    # 调用第三打码平台，云码识别
    ydm = YdmVerify()
    a_zuobiao = ydm.click_verify(image=b64_image, extra="click")  # 219,151|129,78

    # y_data='{"msg":"识别成功","code":10000,"data":{"code":0,"data":"123,159|96,42","time":0.05450940132141113,"unique_code":"240a35dbab289deeb0dcee7a91f9221e"}}'
    # a_zuobiao = cilk_jiyan_a(y_data)  # 219,151|129,78

    # x和y坐标的计算方法 final_x = int(round(x / 333.375 * 100 * 100, 0))

    # a: str = ",".join(i.replace(",", "    _") for i in a_zuobiao.split("|"))
    a: str = ",".join(
        [f"{int(round(float(b[0]) / 333.375 * 100 * 100, 0))}_{int(round(float(b[1]) / 333.375 * 100 * 100, 0))}" for b
         in [i.split(",") for i in a_zuobiao.split("|")]])

    w_params = {
        "c": c,
        "s": s,
        "gt": gt,
        "challenge": challenge,
        "a": a,  # 坐标 8354_1005,1575_1125,1215_7934,4814_3615
        "pic": pic,  # //背景图片地址

    }
    w = open_js_w(w_params)

    time.sleep(1)

    url6 = "https://api.geevisit.com/ajax.php"
    params6 = {
        "gt": gt,
        "challenge": challenge,
        "lang": "zh-cn",
        "pt": "0",
        "client_type": "web",
        "w": w,
        "callback": "geetest_" + str(int(time.time() * 1000))
    }

    data_dict = request_url6(url6, params6)

    session.close()  # 关闭连接
    return data_dict


if __name__ == '__main__':
    resp_validate=main()
    print(resp_validate)
