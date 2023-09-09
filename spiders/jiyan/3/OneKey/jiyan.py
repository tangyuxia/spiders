# -*- coding: utf-8 -*-
# Auther : 风雪
# Date : 2023/3/29 21:41
# File : 把省市区里面的unicode转换为中文.py

import time
import json

import requests

# import subprocess
# from functools import partial  # 这玩意能锁定一个函数的参数
#
# # 锁定subprocess.Popen的encoding参数为"utf-8"
# subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs


class JiYan():
    def __init__(self):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }
        self.index_url = 'https://www.geetest.com/demo/gt/register-fullpage'
        self.jiyan_2_geetest_url = 'https://apiv6.geetest.com/gettype.php'
        self.jiyan3_url = 'https://apiv6.geetest.com/get.php'
        self.jiyan_jajax_url = 'https://api.geevisit.com/ajax.php'

        # self.gt_dict = {
        #     'width': "300px",
        #     'ww': 'true',
        #     'api_server': "apiv6.geetest.com",
        #     # 'cc': 12,
        #     'http': 'true',
        #     'new_captcha': 'true',
        #     'offline': 'false',
        #     'product': "float",
        #     'protocol': "https://",
        #     # 'i': '"6126!!7414!!CSS1Compat!!1!!-1!!-1!!-1!!-1!!-1!!-1!!-1!!-1!!-1!!2!!3!!-1!!-1!!-1!!-1!!-1!!-1!!-1!!-1!!-1!!-1!!1!!-1!!-1!!-1!!0!!0!!0!!0!!233!!929!!1920!!1032!!zh-CN!!zh-CN!!-1!!1!!24!!Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36!!1!!1!!1920!!1080!!1920!!1032!!1!!1!!1!!-1!!Win32!!0!!-8!!8ec1b6326b1ce95da3c79317a3ffdf60!!0!!internal-pdf-viewer,internal-pdf-viewer,internal-pdf-viewer,internal-pdf-viewer,internal-pdf-viewer!!0!!-1!!0!!12!!Arial,ArialBlack,ArialNarrow,Calibri,Cambria,CambriaMath,ComicSansMS,Consolas,Courier,CourierNew,Georgia,Helvetica,Impact,LucidaConsole,LucidaSansUnicode,MicrosoftSansSerif,MSGothic,MSPGothic,MSSansSerif,MSSerif,PalatinoLinotype,SegoePrint,SegoeScript,SegoeUI,SegoeUILight,SegoeUISemibold,SegoeUISymbol,Tahoma,Times,TimesNewRoman,TrebuchetMS,Verdana,Wingdings!!1680112207621!!-1!!-1!!-1!!12!!-1!!-1!!-1!!5!!-1!!-1"',
        # }
        self.request_2_params = {}
        self.request_3_params = {}

        self.crack_params1 = {}
        self.crack_params2 = {}
        self.cookie = {
            "GeeTestUser": 'ce79a7fc6c82455564feb34c756533a6'
        }

    def request_get(self, url, params: dict, headers=None, cookie=None):
        resp = requests.get(url=url, params=params, headers=headers)
        return resp

    def params2(self, get1):
        self.request_2_params['gt'] = get1['gt']
        self.request_2_params['callback'] = 'geetest_' + str(int(time.time() * 1000))

    def params3(self, get1, get2):
        w_dict = {}
        w_dict['gt'] = get1['gt']
        w_dict['challenge'] = get1['challenge']
        w_dict["offline"] = 'false'
        w_dict["new_captcha"] = 'true'
        w_dict["product"] = "float"
        w_dict["width"] = "300px"
        w_dict["https"] = 'true'
        w_dict["api_server"] = "apiv6.geetest.com"
        w_dict["protocol"] = "https://"
        w_dict = dict(w_dict, **get2['data'])
        w_dict["cc"] = 12
        w_dict["ww"] = 'true'

        with open("jiyan_jiyan.js", 'r', encoding='utf-8') as f:
            script = f.read()
            obj = execjs.compile(script)
            # print(w_dict)
            w1 = obj.call('w1',w_dict)

        params3 = {
            'lang': 'zh-cn',
            'pt': '0',
            'client_type': 'web',
        }

        self.request_3_params['gt'] = get1['gt']
        self.request_3_params['challenge'] = get1['challenge']
        self.request_3_params['w'] = w1['w']
        self.request_3_params = dict(params3, **self.request_3_params)
        self.request_3_params['callback'] = 'geetest_' + str(int(time.time() * 1000))
        return w1['nn']

    def parse_jsonp_jiexi(self, data_str_jsonp):
        data_dict = json.loads(data_str_jsonp[data_str_jsonp.index("{"):data_str_jsonp.rindex("}") + 1])
        return data_dict

    def crack_params_fn(self, data: dict, fn=1):
        # 解析jsonp，返回指点格式
        # exec("self.crack_params1 = dict(self.crack_params1, **data['data'])")
        exec("self.crack_params%s = dict(self.crack_params%s, **data['data'])" % (str(fn), str(fn)))
        return data

    def crack_params2_fn(self, data: dict):
        # 解析jsonp，返回指点格式
        data_dict = data['data']
        self.crack_params2 = dict(self.crack_params2, **data_dict)
        return data_dict

    def run(self):
        session = requests.session()
        request_1_params = {'t': str(int(time.time() * 1000))}
        # {'success': 1, 'challenge': '058a8428b9f552af9da07fd6c0781895', 'gt': 'e52c06c937981b90b275d0aff1d40076', 'new_captcha': True}
        resp_get = session.get(url=self.index_url, params=request_1_params, headers=self.headers)
        get1 = resp_get.json()
        # 设置第二次请求的参数
        self.params2(get1)

        # 第二次请求
        resp_get2 = session.get(url=self.jiyan_2_geetest_url, params=self.request_2_params, headers=self.headers)
        # 把jsonp格式处理成dict格式,设置js需要的第一个参数
        get2_json = self.crack_params_fn(self.parse_jsonp_jiexi(resp_get2.text))

        # 第三次请求
        # 设置请求参数
        nn = self.params3(get1, get2_json)

        resp3 = session.get(url=self.jiyan3_url, params=self.request_3_params, headers=self.headers)

        get3_json = self.crack_params_fn(self.parse_jsonp_jiexi(resp3.text), fn=2)


        with open("jiyan_jiyan.js", 'r', encoding='utf-8') as f:
            script = f.read()
        obj = execjs.compile(script)

        gt = self.request_3_params['gt']
        challenge = self.request_3_params['challenge']
        c = self.crack_params2['c']
        s = self.crack_params2['s']

        w = obj.call('w2', gt, challenge, c, s,nn)

        params4=self.request_3_params
        params4['w']=w
        # params4['w']='oJWQKAYeK4C8BFXQUH0MIRfgRE7YVIgvYFW10tTqufX05hyJC9zEeRfWVGSNOfg6YX2OjZwRmTIuSYUb5O7Txl(97ScYLFx1pV4vh09QHdTdJ13AUOGOy6FTJ94AQNkE84vR95Af5YyPkCISm2ZtV)q)s4ffc3dqxEY(MnjbCea4AAi2SS70fOczFVtTiWQOgkdcUNgZNFv3MZ8zM)JOAMCelMUXR12d1VeUATmffK9kjLbXoc0(xBiCXHPYZ)p)Pz6ID5nmdpBkRDXqMyOezdFR3BFhMfPbxUtTztC8iShQ7NHMbeN2A7RmvhDhdf(jFwQVjuef2A2ga9zrf56sMM2MlSFzFNcCgA6B8sVDL48vAVtLx6x86liPivEIZpraQDM1gII5Ab1ZA(fE(LYZuRkocH71Sq5IKLSbNfLOpJVDUUpHf1ohTyzljNyd0IAIuxs7ysPZQduhEpOfwWTqru84Lkz1JE1CzegN7sendaBX9oQ5iAWECWLpOWXcVpCF8weYGv4V79d0elv44bOYVpo147Cbn0jGLeyd(wlqPjLcck8dWiqqv5bhP6y0lpPyp2r7)Co337go8ZgnG5Ch6pJ8bbjBHCH6LjLYRo5d0p6vQxGtSIHxHEYbkPJ5tJ5Lw2M(iC)CrLMzpOamBS3wAbdPTvNKKKfiHPuDvqzia3FPvh1uyZT3GegUUwCmK8xd(uh8x9LOmxXbeme0rbi8MqdMRyXDj))t63Llgs2nzU)Tq3r)YX47tYau3DXznto4KX2rwHUVfSVnzw6jG3R1ChXbVeW6Wx9eCLZ8n6fIcW8exBH2ndZ(qhX(5Cz7FGk600M(PatGJLnBcGBO88aPxalS95)HLUq4ssab2GLL6((AI1rdnI7rTTHyOtqUsMRE2wpnLcdTy8fuz(x3(owHGpyKkikcu8USgz7aMgshKpWZRIYL80WgpxDnltpm)IfNwZwlA4a(ULRURZ0FG443qxA1IUXDQB274xFqZInLEbRV766BfWg2pqLdW(LjqKKzRfMK5LFQKDmooSJptR0Bn9AQrix5pPZpW)TwVllkbvF)D5KU33ewP2NpacW)1ywReqeDO878kZ3E3tduAZBJ0iWr6xjQSGMcT0lHFxupGmKFKAKo0Q3AJ8FjXs2NYq5DfOzFG(rWAcdIblMMIIf(aO6dvG)C95YKXHaG98UTryNMxhJQY9TyU8GTXoHCE10HyjT2ZuTuGD19)DbYsV3lI3NFWPrw(kWR5r2jtIPhSAgKDdok3eBcVBhtGCNJoowHz3xmroKsPyuwb3rES)riFC7qKJ)cPcgw(wDIeY1yu4rkgQXjgZadOmD4C3LiThcUaXELdSjV9cKeTkKlRHZp0W7mBMVjd01FBpIkPMCptiGFOaX7gG6DN5Yr08wgSnxijpZksPuiYqALGnO(anFUdy(5V1w)FyaiYzTMnmYpSY(HQ5UTnDNsTz0D2iAiFmxq93XaMTJG)JqHItjfk1IUr4l0EzIq8RPuRscJXpcCEpyf79naX7E7vJFWS6h6phl8UqeUqr2ge2AIS9Hy0YAGr4BQ2CRTavTwy1rUaDH095HLBoOUTOB7x3jV3pic(yhr'

        get4 = session.get(url=self.jiyan_jajax_url, params=params4, headers=self.headers,cookies=self.cookie)
        return get4.text


if __name__ == '__main__':
    jiyan = JiYan()
    # jiyan.get_gt()
    success = jiyan.run()
    print(success)
