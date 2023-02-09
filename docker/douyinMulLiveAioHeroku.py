# -*- coding: utf-8 -*-
# @Time    : 2022/1/14 15:18
# @Author  : muyangren907
# @Email   : myr907097904@gmail.com
# @File    : douyinMulLiveAioHeroku.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time    : 2022/1/5 10:17
# @Author  : muyangren907
# @Email   : myr907097904@gmail.com
# @File    : douyinMulLiveAio.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time    : 2022/1/4 11:00
# @Author  : muyangren907
# @Email   : myr907097904@gmail.com
# @File    : douyinAiotest.py
# @Software: PyCharm
# 协程获取下载链接
# 多线程下载
import asyncio
import configparser
import json
import logging
import os
import re
import shutil
import subprocess
import threading
import time
import traceback
import requests

import aiohttp
import base64


def base64encode(s):
    en = base64.b64encode(s.encode('utf-8'))
    return en.decode('utf-8')


def base64decode(a):
    de = base64.b64decode(a)
    return de.decode('utf-8')


from urllib.parse import unquote


def urldecode(strin):
    text = unquote(strin, 'utf-8')
    return text


import logging  # 引入logging模块

# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级开关

# 第二步，创建一个handler，用于写入日志文件
# log_path = os.path.dirname(os.getcwd()) + '/Logs/'
# log_name = log_path + 'log.log'
# logfile = 'log.txt'
# file_handler = logging.FileHandler(logfile, mode='a+')
# file_handler.setLevel(logging.DEBUG)  # 输出到file的log等级的开关

# 第三步，定义handler的输出格式
formatter = logging.Formatter(
    "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
# file_handler.setFormatter(formatter)

# 第四步，将handler添加到logger里面
# logger.addHandler(file_handler)

# 如果需要同時需要在終端上輸出，定義一個streamHandler
p_handler = logging.StreamHandler()  # 往屏幕上输出
p_handler.setFormatter(formatter)  # 设置屏幕上显示的格式
logger.addHandler(p_handler)


def strfomat(str_in):
    sub_str = re.sub(
        u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", str_in)
    return sub_str


def sleep_dis(sleep_time):
    for i in range(sleep_time, -1, -1):
        print('休眠 %5s s' % i, end='\r')
        time.sleep(1)


async def subwords(words):
    words = re.sub('[? * : " < >  / |]', '', words)
    words = re.sub(r'\\', '', words)
    return words


async def get_roomid(html):
    try:
        data0 = html['data']['data'][0]
        stream_url = data0['stream_url']
        id_str = data0['id_str']
        return id_str
    except Exception as e:
        return -1
    # # js = re.findall(r"<script>(.{666,}?)</script>", html)[0]
    # js = re.findall(r'<script id="RENDER_DATA" type="application/json">(.{666,}?)</script>', html)[0]
    # print(js)
    # ret = json.loads(js.replace("window.__INIT_PROPS__ = ", ""))
    # if "room" in ret["/webcast/reflow/:id"] and 'own_room' not in ret["/webcast/reflow/:id"]["room"]["owner"]:
    #     return -1
    # else:
    #     return ret["/webcast/reflow/:id"]["room"]["owner"]["own_room"]["room_ids_str"][0]

    # if "room" in html["data"] and 'own_room' not in html["data"]["room"]["owner"]:
    #     return -1
    # else:
    #     return (html["data"]["room"]["owner"]["own_room"]["room_ids_str"][0])


async def get_nickname(html):
    return html["data"]["user"]["nickname"]
    # return html["data"]["room"]["owner"]['nickname']
    # js = re.findall(r"<script>(.{666,}?)</script>", html)[0]
    # ret = json.loads(js.replace("window.__INIT_PROPS__ = ", ""))
    # return ret["/webcast/reflow/:id"]["room"]["owner"]["nickname"]


async def get_status(html):
    return -1
    # return html["data"]["room"]["status"]
    # js = re.findall(r"<script>(.{666,}?)</script>", html)[0]
    # ret = json.loads(js.replace("window.__INIT_PROPS__ = ", ""))
    # return ret["/webcast/reflow/:id"]["room"]["status"]


async def get_urls(html):
    # js = re.findall(r"<script>window.__INIT_PROPS__ =(.{666,}?)</script>", html)[0]
    # ret = json.loads(js.replace("<script>window.__INIT_PROPS__ = ", ""))
    # # ["room"]["stream_url"]['rtmp_pull_url']
    # return ret["/webcast/reflow/:id"]["room"]["stream_url"]['rtmp_pull_url']
    # try:
    data0 = html['data']['data'][0]
    stream_url = data0['stream_url']
    flv_pull_url = stream_url['flv_pull_url']
    ret_url = flv_pull_url['FULL_HD1']
    # id_str = data0['id_str']
    return ret_url
    # except Exception as e:
    #     return -1
    # return html["data"]["room"]["stream_url"]['rtmp_pull_url']


async def get_jiaodihuazhiurl(html):
    # js = re.findall(r"<script>window.__INIT_PROPS__ =(.{666,}?)</script>", html)[0]
    # ret = json.loads(js.replace("<script>window.__INIT_PROPS__ = ", ""))
    huazhis = ['HD1', 'SD1', 'SD2']
    # flv_pull_url = ret["/webcast/reflow/:id"]["room"]["stream_url"]['flv_pull_url']
    flv_pull_url = html["data"]["room"]["stream_url"]['flv_pull_url']
    for huazhi in huazhis:
        if huazhi in flv_pull_url:
            logger.info('返回 {} 画质'.format(huazhi))
            return flv_pull_url[huazhi]
    logger.info('渣画质不存在,返回原始画质')
    return get_urls(html)


# 处理单个url的函数
async def get(session, queue):
    global ids_running
    Modelheaders = {
        # 'upgrade-insecure-requests':'1',
        # 'X-Forwarded-For': genip(),
        # 'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36'
        # 'User-Agent':'Mozilla/5.0 (Linux; U; Android 8.1.0; en-US; Nexus 6P Build/OPM7.181205.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.11.1.1197 Mobile Safari/537.36'
        'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.34',
    }
    Modelheaders = {
        'authority':
            'live.douyin.com',
        'accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language':
            'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control':
            'max-age=0',
        # 'cookie': 'xgplayer_user_id=484396791271; session_secure=1; ttwid=1%7Cv70bMg0H26eflXmeq7YexUhnTLwoWLJClBtqIYPqZE8%7C1669296852%7C323fd8a92941d04abc8b14ea38553fa317b9462c7c474c6b98ac63fe1f5add70; d_ticket=687002b130aebc2c765d4d585ce9dccc34880; sso_auth_status=7f399ac96a5e4afdebee0d53002c61cb; sso_auth_status_ss=7f399ac96a5e4afdebee0d53002c61cb; csrf_session_id=0cb567954252b310166550749f7612ab; passport_fe_beating_status=true; passport_csrf_token=d59892d74c3ae2800954153ebf8a5aba; passport_csrf_token_default=d59892d74c3ae2800954153ebf8a5aba; n_mh=2awS99UZxOYCYMo9gqgsAxEu-NVaJYeU5MIm8TrCZRY; passport_assist_user=CkEdZhs9Exqlbjr1x2FWd8xPTRi7MoKCHPO6-DbDnUohFD684OjDs1eqioZXY4AcVYZ1VtzKbnI96yqlwFWtx7_WGhpICjzs42VP7ulFaqVxKQxyCQuhl9VRumoBxk0Y8dUR9oMCt2F8dJmQZ9Q4tNscrcmGywpCu8G3WD5scPF0wCkQ4tikDRiJr9ZUIgED2pEOZw%3D%3D; sso_uid_tt=270676b34399fbff50c3fdaf033fc2c6; sso_uid_tt_ss=270676b34399fbff50c3fdaf033fc2c6; toutiao_sso_user=adec5c4429c05b858819ea01845c8725; toutiao_sso_user_ss=adec5c4429c05b858819ea01845c8725; sid_ucp_sso_v1=1.0.0-KDcxMjk2ZmYyOWViZWYxYjNlMDA3YTI3NWQ2ZmNkNGZlOTA2ZWQ0NDcKHwjcpbDY6vS3AhCr65qdBhjvMSAMMJqBq_sFOAZA9AcaAmhsIiBhZGVjNWM0NDI5YzA1Yjg1ODgxOWVhMDE4NDVjODcyNQ; ssid_ucp_sso_v1=1.0.0-KDcxMjk2ZmYyOWViZWYxYjNlMDA3YTI3NWQ2ZmNkNGZlOTA2ZWQ0NDcKHwjcpbDY6vS3AhCr65qdBhjvMSAMMJqBq_sFOAZA9AcaAmhsIiBhZGVjNWM0NDI5YzA1Yjg1ODgxOWVhMDE4NDVjODcyNQ; odin_tt=0f87a216705efe6993ac588188740708c56cca553c9d79938f3e2975ada4a982797a8717fdbbfede5671ffdb1b994a869b324ba4ec6d518f9e14468b471c41b0; passport_auth_status=80a6904fddf2ebd984fa21a8e85358a2%2Cdd63326f6f4519387766488788799563; passport_auth_status_ss=80a6904fddf2ebd984fa21a8e85358a2%2Cdd63326f6f4519387766488788799563; uid_tt=3846eb60ac9d17a6165a6f764235b50e; uid_tt_ss=3846eb60ac9d17a6165a6f764235b50e; sid_tt=5a3a9c8563dbeccbb9014db8ce9a675e; sessionid=5a3a9c8563dbeccbb9014db8ce9a675e; sessionid_ss=5a3a9c8563dbeccbb9014db8ce9a675e; LOGIN_STATUS=1; sid_guard=5a3a9c8563dbeccbb9014db8ce9a675e%7C1671869872%7C5183995%7CWed%2C+22-Feb-2023+08%3A17%3A47+GMT; sid_ucp_v1=1.0.0-KDU1NjRmNDAwNmFhOGNhMjA1NWI5MDA3MTZhMGQ4YTkyNTM2YWVkNDAKGQjcpbDY6vS3AhCw65qdBhjvMSAMOAZA9AcaAmhsIiA1YTNhOWM4NTYzZGJlY2NiYjkwMTRkYjhjZTlhNjc1ZQ; ssid_ucp_v1=1.0.0-KDU1NjRmNDAwNmFhOGNhMjA1NWI5MDA3MTZhMGQ4YTkyNTM2YWVkNDAKGQjcpbDY6vS3AhCw65qdBhjvMSAMOAZA9AcaAmhsIiA1YTNhOWM4NTYzZGJlY2NiYjkwMTRkYjhjZTlhNjc1ZQ; download_guide=%223%2F20221224%22; FOLLOW_RED_POINT_INFO=%221%22; SEARCH_RESULT_LIST_TYPE=%22single%22; home_can_add_dy_2_desktop=%220%22; strategyABtestKey=%221671906320.331%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAIpvieueUTPWlnUPC4BAnBlDORKstHlr4XgjX1hBFlgtwYNfiFDF3aDsIzLCbwanI%2F1671984000000%2F0%2F1671950215375%2F0%22; __ac_nonce=063a7ef9300183c0c1c3b; __ac_signature=_02B4Z6wo00f01uPrLXgAAIDCY-nXOoiU277jzynAANtqKyFzXsgIH2i98fwWU0jwl5R4k0ctLdNfPQlizWT892-AaC5Rc7WYrCeTPaLlUW1j8igjYrns4AhtWGwPlz-4pS5hFO9VKyg0SYRm0c; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAIpvieueUTPWlnUPC4BAnBlDORKstHlr4XgjX1hBFlgtwYNfiFDF3aDsIzLCbwanI%2F1671984000000%2F0%2F1671951350975%2F0%22; msToken=3XDQ_VZ3g-lJ68o_XYi7AoV5sSH7iha08-K0pGNq_RAwUlu83WRA4lEHbeo8Dk2zt21oO0iFO_1e_lv3t98bC4AIzgNFHbcOBr2gwBfLe7fzxeUCXIN7VkCu9aIk-j-eyao=; live_can_add_dy_2_desktop=%220%22; tt_scid=exbhwpioFK3mrbGX6sf-KZpWiK-KcLY1Av2Fmx9tRNU-W4seiXlHURfE6vBFPUTY8dcb; msToken=4PYtrUpMD1KofBdHoo5UfaM9XTZWM-LwAitLOi6rs1FT8tBZl7AbAe9o4CUPb6fjLCOzsSRyIPgmL5pVz0GRh4ohma5o_wX6iRgN0G09liEPdJfhU_p832ortJW-W1ITBKA=',
        'dnt':
            '1',
        'sec-ch-ua':
            '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile':
            '?0',
        'sec-ch-ua-platform':
            '"Windows"',
        'sec-fetch-dest':
            'document',
        'sec-fetch-mode':
            'navigate',
        'sec-fetch-site':
            'none',
        'sec-fetch-user':
            '?1',
        'upgrade-insecure-requests':
            '1',
        'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }
    headers = {
        'authority':
            'live.douyin.com',
        'accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language':
            'zh-CN,zh;q=0.9',
        'cache-control':
            'max-age=0',
        # 'cookie': 'ttwid=1%7CFa3gU4c8VUgp3Hr4V14Vbw5-WlrdMCGazA6_f3bPcPo%7C1671869734%7C01ddb899f14522e87015515e885b0d43c3025cf7b6a7ccdc5054c9cce3ba814d; live_can_add_dy_2_desktop=%220%22; csrf_session_id=b105c42d0e79cb744b39325192f6c8a3; xgplayer_user_id=49845986568; odin_tt=e338b14b54a763adb09b09ad788f215a1a8a776474ada37e4e3f713586a3b23d8a934f600d330610674d65f28ed0450a2a0a341ac73f74f9ce48d2c7fb2a07788475430c5460b1979c55188e8056ce3a; ttcid=80517f7c93ee4e53a4f4998642fcbe9e57; download_guide=%223%2F20221224%22; home_can_add_dy_2_desktop=%220%22; passport_csrf_token=64491208e4cd342759363ed725abe523; passport_csrf_token_default=64491208e4cd342759363ed725abe523; __ac_signature=_02B4Z6wo00f0108SwEwAAIDDzxA6DVijXDtPMsTAALBuK6lVn2--xbCV0k-JziXoGp.azNm0ReC9w.4cm8VpbkAPBtme8nVIJk8iDs5yKQJJaykAozIY2mqvgFMVJxrdDA2leYgrXvpqKjlcf7; SEARCH_RESULT_LIST_TYPE=%22single%22; tt_scid=py1Mmake89.y8D4moozj18Bw39a3WqMPmZDeYI-HZYGFbbNS6U84CpbhlLgkYKK-3cb1; strategyABtestKey=%221671895757.267%22; msToken=QJL_W3D8ijHWgwuFB2xztDHthXVql1dcqFRKtyogVjsia-VsFeNCf10nyk8axIVRdWoTxI75rC28cK9xk3NYR23e2z9kdIv2IFS9TM3yJ7gOHvzsfji1HJg_czklbP8=; msToken=GVwLKsFa70M0oZqD4HuTsT4PCxtqS8QWmCjHeuJJTsQFztll4cLuo9890afSYA__RwgzfZhQmsZ2CGJ1l2H1q3WAA2XgF-aEfIDA8rfclkWHlg2xRVfyNvPy1fnyenc=',
        'dnt':
            '1',
        'sec-ch-ua':
            '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile':
            '?0',
        'sec-ch-ua-platform':
            '"Windows"',
        'sec-fetch-dest':
            'document',
        'sec-fetch-mode':
            'navigate',
        'sec-fetch-site':
            'none',
        'sec-fetch-user':
            '?1',
        'upgrade-insecure-requests':
            '1',
        'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }
    cookies = {
        'ttwid':
            '1%7CFa3gU4c8VUgp3Hr4V14Vbw5-WlrdMCGazA6_f3bPcPo%7C1671869734%7C01ddb899f14522e87015515e885b0d43c3025cf7b6a7ccdc5054c9cce3ba814d',
        'live_can_add_dy_2_desktop':
            '%220%22',
        'csrf_session_id':
            'b105c42d0e79cb744b39325192f6c8a3',
        'xgplayer_user_id':
            '49845986568',
        'odin_tt':
            'e338b14b54a763adb09b09ad788f215a1a8a776474ada37e4e3f713586a3b23d8a934f600d330610674d65f28ed0450a2a0a341ac73f74f9ce48d2c7fb2a07788475430c5460b1979c55188e8056ce3a',
        'ttcid':
            '80517f7c93ee4e53a4f4998642fcbe9e57',
        'download_guide':
            '%223%2F20221224%22',
        'home_can_add_dy_2_desktop':
            '%220%22',
        'passport_csrf_token':
            '64491208e4cd342759363ed725abe523',
        'passport_csrf_token_default':
            '64491208e4cd342759363ed725abe523',
        '__ac_signature':
            '_02B4Z6wo00f0108SwEwAAIDDzxA6DVijXDtPMsTAALBuK6lVn2--xbCV0k-JziXoGp.azNm0ReC9w.4cm8VpbkAPBtme8nVIJk8iDs5yKQJJaykAozIY2mqvgFMVJxrdDA2leYgrXvpqKjlcf7',
        'SEARCH_RESULT_LIST_TYPE':
            '%22single%22',
        'tt_scid':
            'py1Mmake89.y8D4moozj18Bw39a3WqMPmZDeYI-HZYGFbbNS6U84CpbhlLgkYKK-3cb1',
        'strategyABtestKey':
            '%221671895757.267%22',
        'msToken':
            'QJL_W3D8ijHWgwuFB2xztDHthXVql1dcqFRKtyogVjsia-VsFeNCf10nyk8axIVRdWoTxI75rC28cK9xk3NYR23e2z9kdIv2IFS9TM3yJ7gOHvzsfji1HJg_czklbP8=',
        'msToken':
            'GVwLKsFa70M0oZqD4HuTsT4PCxtqS8QWmCjHeuJJTsQFztll4cLuo9890afSYA__RwgzfZhQmsZ2CGJ1l2H1q3WAA2XgF-aEfIDA8rfclkWHlg2xRVfyNvPy1fnyenc=',
    }
    js_headers = {
        # 'upgrade-insecure-requests':'1',
        # 'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Mobile Safari/537.36'
        'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.34',
    }
    while True:
        try:
            share_url = queue.get_nowait()
        except asyncio.QueueEmpty:
            return
        nickname_txt = ids_dic[share_url]
        logger.info('{} {}'.format(nickname_txt, share_url))
        res_html = ''
        try_time = 0
        try_max = 2
        while True:
            try:
                try_time += 1
                # res = await session.get(share_url, headers=Modelheaders, timeout=10)
                # resurl = str(res.url)
                # roomid = ((resurl).split('/')[-1]).split('?')[0]
                # print(resurl)
                # print('{}'.format(roomid))
                # print('{}'.format(res.history))

                # res_html = await res.text()
                # logger.info(share_url)
                # exit(0)
                # spos_str = 'type="application/json">%7B%22'
                # epos_str = '</script>'
                # spos_idx = res_html.index(spos_str)+len('type="application/json">')
                # epos_idx = res_html[spos_idx:].index(epos_str)
                # res_json_ec = res_html[spos_idx:spos_idx+epos_idx]
                # res_json_str = urldecode(res_json_ec)
                # res_json = json.loads(res_json_str)
                # logger.info(res_json_str)
                # time.sleep(90)

                # logger.info(res.url)
                # resurl = str(res.url)
                # roomid = ((resurl).split('/')[-1]).split('?')[0]
                # print('{}'.format(roomid))
                web_rid = share_url
                # jsurl = 'https://live.douyin.com/webcast/web/enter/?aid=6383&web_rid={}'.format(
                #   web_rid)
                jsurl = 'https://live.douyin.com/webcast/room/web/enter/?aid=6383&web_rid={}'.format(web_rid)
                # jsurl = "https://webcast.amemv.com/webcast/room/reflow/info/?type_id=0&live_id=1&room_id=" + roomid + "&app_id=1128&verifyFp=verify_l7rjcs0w_v8JHPZG6_dMDh_4DdV_8Tah_ulpH9Cc9ljkq&sec_user_id=&msToken=EAgLgmWAd9KyOEnKwVwEn1q9nLpgepI9PcP8If7OpX0ApspZ3cVxwh3AopWkX8sbeT9YoIsD3F5zjo12ClWKxQ5UTPfmwdIa0xrKH8X2nh_M9lHlOa0dfPgOS8AOaA==&X-Bogus=DFSzswVO61iANaewSM5chl9WX7ra"
                # jsurl = 'https://live.douyin.com/{}'.format(web_rid)
                logger.info(jsurl)

                res_js = await session.get(jsurl,
                                           headers=Modelheaders,
                                           cookies=cookies,
                                           timeout=10)
                res_html = await res_js.text()
                res_html = str(res_html)
                # print('{}'.format(res_html))
                res_html = json.loads(res_html)
                # exit(0)

                if res_html != '':
                    break
                else:
                    logger.info('{}获取失败 2秒后重试'.format(ids_dic[share_url]))
                    if try_time == try_max:
                        logger.info('{}获取失败 退出'.format(ids_dic[share_url]))
                        ids_running[share_url] = False
                        return
                    sleep_dis(2)
            except Exception as e:
                # traceback.print_exc()
                logger.info('{}'.format(traceback.format_exc()))
                if try_time == try_max:
                    logger.info('{}获取错误 退出'.format(ids_dic[share_url]))
                    ids_running[share_url] = False
                    return
        # print(res_html)

        res_roomid = await get_roomid(res_html)
        # print('res_roomid {}'.format(res_roomid))
        # return
        # logger.info('{} 1111'.format(res_html))
        res_nickname = await get_nickname(res_html)
        res_nickname = strfomat(res_nickname)
        if res_roomid == -1:
            logger.info('{} 未在直播'.format(res_nickname))
            ids_running[share_url] = False
            return
        # print(res_roomid)

        # print(res_nickname)
        # res_status = await get_status(res_html)
        # res_urls = await get_urls(res_html)
        # room_url = 'https://webcast.amemv.com/webcast/reflow/{}'.format(res_roomid)
        # room_url = "https://webcast.amemv.com/webcast/room/reflow/info/?type_id=0&live_id=1&room_id={}&app_id=1128&verifyFp=verify_l7rjcs0w_v8JHPZG6_dMDh_4DdV_8Tah_ulpH9Cc9ljkq&sec_user_id=&msToken=EAgLgmWAd9KyOEnKwVwEn1q9nLpgepI9PcP8If7OpX0ApspZ3cVxwh3AopWkX8sbeT9YoIsD3F5zjo12ClWKxQ5UTPfmwdIa0xrKH8X2nh_M9lHlOa0dfPgOS8AOaA==&X-Bogus=DFSzswVO61iANaewSM5chl9WX7ra".format(
        #     res_roomid)
        # res = await session.get(room_url, headers=Modelheaders, proxy=proxies2, timeout=30)
        # res_html = await res.text()

        # res_html = ''
        try_time = 0
        try_max = 2
        while True:
            try:
                try_time += 1
                # res = await session.get(room_url, headers=Modelheaders, timeout=10)
                # res_html = await res.text()
                # res_html = await res_js.text()
                # res_html = str(res_html)
                # exit(0)
                # print(res_html)
                # logger.info("{}".format(room_url))
                # res_html = json.loads(res_html)
                if res_html != '':
                    break
                else:
                    logger.info('{}获取失败 2秒后重试'.format(ids_dic[share_url]))
                    if try_time == try_max:
                        logger.info('{} 获取失败 退出'.format(ids_dic[share_url]))
                        ids_running[share_url] = False
                        return
                    sleep_dis(2)
            except Exception as e:
                # traceback.print_exc()
                logger.info('{}'.format(traceback.format_exc()))
                if try_time == try_max:
                    logger.info('{} 获取错误 退出'.format(ids_dic[share_url]))
                    ids_running[share_url] = False
                    return

        res_roomid = await get_roomid(res_html)
        res_status = await get_status(res_html)
        res_urls = await get_urls(res_html)
        logger.info('获取成功 {} {} {} {} {} {}'.format(share_url, nickname_txt,
                                                        res_roomid, res_nickname,
                                                        res_status, res_urls))
        dlthread = DLThread(share_url, nickname_txt, res_roomid, res_nickname,
                            res_status, res_urls)
        dlthread.start()


def getherokuargs(query_type):
    # h_url = 'https://owziotrlotjimdv.herokuapp.com/api?query_type={}'.format(query_type)
    h_url = 'https://raw.githubusercontent.com/xiaosijitest/weioferiogeroijiii/main/{}.txt'.format(
        query_type)

    trytime = 0
    while True:
        trytime += 1
        try:
            logger.info('{}'.format(h_url))
            res = requests.get(h_url, timeout=10)
            # logger.info('{}'.format(res))
            # resjson = res.json()
            res_text = res.text
            logger.info('{}'.format(res_text))
            if True:
                ret_str = res.text
                break
            else:
                logger.info('获取参数失败 2秒后再试')
                sleep_dis(2)
        except Exception as e:
            traceback.print_exc()
            time.sleep(5)
    return ret_str


# async def getcookies():
#     # cookiesstr = os.environ.get("cookies")
#     cookiesstr = getherokuargs("kscookies")
#     cookiesstr = base64decode(cookiesstr)
#     keyvals = cookiesstr.split('&&&&')
#     cookiesobj = {
#     }
#     for keyval in keyvals:
#         if '&&&' not in keyval:
#             continue
#         key, val = keyval.split('&&&')
#         cookiesobj[key] = val
#     return cookiesobj
# 修改
def get_ids():
    # 特定id文件特定处理
    ids_dic = {}
    # ids_gen = await session.get(jsurl, headers=Modelheaders, timeout=10)
    # 'test_web'
    # ids_gen = getherokuargs('test_web')
    # ids_gen = 'ODM5NDA5MTgwNjQs5Li75pKtOiDljZbovabnvo7lpbNf5bCP5p2o5aa5'
    if debugmode:
        ids_gen = getherokuargs('test_web')
    else:
        ids_gen = getherokuargs('douyinzhibo04_web')
    # ids_gen = os.environ.get("ids_str")
    ids_str = base64decode(ids_gen)
    # with open(ids_txt, mode='r', encoding='utf-8') as ids_f:
    #     ids_str = ids_f.read()
    ids_list = ids_str.split('\n')
    for id_line in ids_list:
        if id_line != '' and ',主播:' in id_line:
            id_s = id_line.split(',主播: ')
            live_url = id_s[0]
            nickname = id_s[1]
            ids_dic[live_url] = nickname

    return ids_dic


async def main():
    global ids_dic
    # global proxies2
    # global proxies2ip
    global luzhishichang
    global videopath
    global luzhi_ok_path
    while True:
        ids_dic = get_ids()

        try:
            # config = configparser.ConfigParser()
            # config.read('config.ini', encoding='utf-8-sig')
            # proxies2 = config.get('1', '代理端口')
            # proxies2ip = config.get('1', '代理ip')
            # luzhishichang = config.get('1', 'luzhishichang')
            # videopath = config.get('1', '直播保存路径')
            # luzhi_ok_path = config.get('1', 'luzhi_ok_path')
            logger.info('录制保存路径 {}'.format(videopath))
            logger.info('录制成功保存路径 {}'.format(luzhi_ok_path))
            proxies2 = ''
            proxiesn = proxies2

            if len(proxies2) > 0:
                proxies2 = 'http://{}:{}'.format(proxies2ip, proxiesn)
                logger.info("设置代理地址为: " + 'http://{}:{}'.format(proxies2ip, proxiesn))
            else:
                proxies2 = ""
                logger.info("无代理")
        except Exception as e:
            # traceback.print_exc()
            sleep_dis(SLEEP_TIME)
            continue

        queue = asyncio.Queue()
        # print(ids_dic)
        for id__ in ids_dic:
            if id__ not in ids_running:
                logger.info('{} 加入录制'.format(ids_dic[id__]))
                queue.put_nowait(id__)
                ids_running[id__] = True
            elif ids_running[id__] == False:
                logger.info('{} 未在录制'.format(ids_dic[id__]))
                queue.put_nowait(id__)
                ids_running[id__] = True
            else:
                luzhimp4s = [mp4_ for mp4_ in os.listdir('luzhi') if '.mp4' in mp4_]
                dlf = False
                for ijk in luzhimp4s:
                    if ids_dic[id__] in ijk:
                        logger.info('{} 已在录制'.format(ids_dic[id__]))
                        dlf = True
                        break
                if not dlf:
                    queue.put_nowait(id__)
                    ids_running[id__] = True

        tasks = []
        async with aiohttp.ClientSession() as session:
            for _ in range(len(ids_dic)):
                task = get(session, queue)
                tasks.append(task)
            await asyncio.wait(tasks)
        sleep_dis(SLEEP_TIME)


# 关于同时录制
class DLThread(threading.Thread):

    def __init__(self, share_url, nickname_txt, res_roomid, res_nickname,
                 res_status, res_urls):
        threading.Thread.__init__(self)
        self.share_url = share_url
        self.nickname_txt = nickname_txt
        self.res_roomid = res_roomid
        self.res_nickname = res_nickname
        self.res_status = res_status
        self.res_urls = res_urls

    def run(self):
        global dlrids
        global notlivings
        dynjmvzylz_path = "dynjmvzylz"
        trytime = 0
        trymax = 5
        while True:
            try:
                logger.info('开始录制 {} {} {} {}'.format(self.res_roomid,
                                                          self.res_nickname,
                                                          self.res_status, self.res_urls))

                now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
                filename = '{}_{}_{}.mp4'.format(self.nickname_txt, self.res_nickname,
                                                 now)
                # filename = '{}.mp4'.format(base64encode(filename))
                file = os.path.join(videopath, filename)
                if not os.path.exists(videopath):
                    os.makedirs(videopath)
                _output = subprocess.check_output(
                    'dynjmvzylz -y -v verbose -rw_timeout 10000000 -loglevel error -hide_banner -analyzeduration 2147483647 -probesize 2147483647 -i "{}" -fs 1500M -t {} -bufsize 5000k -map 0 -sn -dn -c:v copy -max_muxing_queue_size 2048 "{}"'
                    .format(self.res_urls, luzhishichang, file),
                    stderr=subprocess.STDOUT,
                    shell=True)
                trytime = 1
                if not os.path.exists(luzhi_ok_path):
                    os.makedirs(luzhi_ok_path)
                shutil.move(file, luzhi_ok_path)
                logger.info('分段录制结束 {} {} {} {}'.format(self.res_roomid,
                                                              self.res_nickname,
                                                              self.res_status,
                                                              self.res_urls))
            except Exception as e:
                traceback.print_exc()
                trytime += 1

                logger.info('遇到错误 录制结束 {} {} {} {}'.format(self.res_roomid,
                                                                   self.res_nickname,
                                                                   self.res_status,
                                                                   self.res_urls))
                if trytime == trymax:
                    ids_running[self.share_url] = False
                    return


if __name__ == '__main__':
    '''
      ids_str heroku读取
      luzhishichang 1800
      videopath luzhi
      luzhi_ok_path luzhichenggong
      '''
    # ids_gen = os.environ.get("ids_str")
    # proxies2 = config.get('1', '代理端口')
    # proxies2ip = config.get('1', '代理ip')
    debugmode = False
    luzhishichang = os.environ.get("luzhishichang")
    luzhishichang = 600
    videopath = 'luzhi'
    luzhi_ok_path = "luzhichenggong"
    logger.info('luzhishichang {}'.format(luzhishichang))

    ids_dic = {}
    ids_running = {}
    proxies2 = {}
    # videopath = ''
    # luzhi_ok_path = ''
    # luzhishichang = 1800
    # ids_file_path = 'URL_config.ini'
    # ids_file_path = 'ids.txt'
    SLEEP_TIME = 60
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
