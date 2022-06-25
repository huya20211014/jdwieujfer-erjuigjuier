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
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
# file_handler.setFormatter(formatter)

# 第四步，将handler添加到logger里面
# logger.addHandler(file_handler)


# 如果需要同時需要在終端上輸出，定義一個streamHandler
p_handler = logging.StreamHandler()  # 往屏幕上输出
p_handler.setFormatter(formatter)  # 设置屏幕上显示的格式
logger.addHandler(p_handler)


def strfomat(str_in):
    sub_str = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", str_in)
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

    # # js = re.findall(r"<script>(.{666,}?)</script>", html)[0]
    # js = re.findall(r'<script id="RENDER_DATA" type="application/json">(.{666,}?)</script>', html)[0]
    # print(js)
    # ret = json.loads(js.replace("window.__INIT_PROPS__ = ", ""))
    # if "room" in ret["/webcast/reflow/:id"] and 'own_room' not in ret["/webcast/reflow/:id"]["room"]["owner"]:
    #     return -1
    # else:
    #     return ret["/webcast/reflow/:id"]["room"]["owner"]["own_room"]["room_ids_str"][0]

    if "room" in html["data"] and 'own_room' not in html["data"]["room"]["owner"]:
        return -1
    else:
        return (html["data"]["room"]["owner"]["own_room"]["room_ids_str"][0])


async def get_nickname(html):
    return html["data"]["room"]["owner"]['nickname']
    # js = re.findall(r"<script>(.{666,}?)</script>", html)[0]
    # ret = json.loads(js.replace("window.__INIT_PROPS__ = ", ""))
    # return ret["/webcast/reflow/:id"]["room"]["owner"]["nickname"]


async def get_status(html):
    return html["data"]["room"]["status"]
    # js = re.findall(r"<script>(.{666,}?)</script>", html)[0]
    # ret = json.loads(js.replace("window.__INIT_PROPS__ = ", ""))
    # return ret["/webcast/reflow/:id"]["room"]["status"]


async def get_urls(html):
    # js = re.findall(r"<script>window.__INIT_PROPS__ =(.{666,}?)</script>", html)[0]
    # ret = json.loads(js.replace("<script>window.__INIT_PROPS__ = ", ""))
    # # ["room"]["stream_url"]['rtmp_pull_url']
    # return ret["/webcast/reflow/:id"]["room"]["stream_url"]['rtmp_pull_url']
    return html["data"]["room"]["stream_url"]['rtmp_pull_url']



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
async def get(session,queue):
    Modelheaders = {
        # 'upgrade-insecure-requests':'1',
        # 'X-Forwarded-For': genip(),
        # 'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36'
        'User-Agent':'Mozilla/5.0 (Linux; U; Android 8.1.0; en-US; Nexus 6P Build/OPM7.181205.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.11.1.1197 Mobile Safari/537.36'
    }
    js_headers = {
        # 'upgrade-insecure-requests':'1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Mobile Safari/537.36'
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
                res = await session.get(share_url, headers=Modelheaders, timeout=10)
                # logger.info(res.url)
                resurl = str(res.url)
                roomid = ((resurl).split('/')[-1]).split('?')[0]
                # print(''.format(roomid))
                jsurl = "https://webcast.amemv.com/webcast/room/reflow/info/?type_id=0&live_id=1&room_id=" + roomid + "&app_id=1128"
                res_js = await session.get(jsurl, headers=Modelheaders, timeout=10)
                res_html = await res_js.text()
                res_html = str(res_html)
                # print(res_html)
                res_html = json.loads(res_html)
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
        room_url = "https://webcast.amemv.com/webcast/room/reflow/info/?type_id=0&live_id=1&room_id={}&app_id=1128".format(res_roomid)
        # res = await session.get(room_url, headers=Modelheaders, proxy=proxies2, timeout=30)
        # res_html = await res.text()

        res_html = ''
        try_time = 0
        try_max = 2
        while True:
            try:
                try_time += 1
                res = await session.get(room_url, headers=Modelheaders, timeout=10)
                res_html = await res.text()
                # res_html = await res_js.text()
                res_html = str(res_html)
                # print(res_html)
                res_html = json.loads(res_html)
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
        logger.info('获取成功 {} {} {} {} {} {}'.format(share_url, nickname_txt, res_roomid, res_nickname, res_status, res_urls))
        dlthread = DLThread(share_url, nickname_txt, res_roomid, res_nickname, res_status, res_urls)
        dlthread.start()


def getherokuargs(query_type):
    # h_url = 'https://owziotrlotjimdv.herokuapp.com/api?query_type={}'.format(query_type)
    h_url = 'https://raw.githubusercontent.com/xiaosijitest/weioferiogeroijiii/main/{}.txt'.format(query_type)

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
#修改
def get_ids():
    # 特定id文件特定处理
    ids_dic = {}
    # ids_gen = await session.get(jsurl, headers=Modelheaders, timeout=10)
    ids_gen = getherokuargs('douyinzhibo24_ids_str')
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
            if id__ not in ids_running or ids_running[id__] == False:
                queue.put_nowait(id__)
                ids_running[id__] = True
            else:
                logger.info('{} 已在录制'.format(ids_dic[id__]))
        tasks = []
        async with aiohttp.ClientSession() as session:
            for _ in range(len(ids_dic)):
                task = get(session,queue)
                tasks.append(task)
            await asyncio.wait(tasks)
        sleep_dis(SLEEP_TIME)


# 关于同时录制
class DLThread(threading.Thread):
    def __init__(self, share_url, nickname_txt, res_roomid, res_nickname, res_status, res_urls):
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
                logger.info('开始录制 {} {} {} {}'.format(self.res_roomid, self.res_nickname, self.res_status, self.res_urls))

                now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
                filename = '{}_{}_{}.mp4'.format(self.nickname_txt, self.res_nickname, now)
                # filename = '{}.mp4'.format(base64encode(filename))
                file = os.path.join(videopath, filename)
                if not os.path.exists(videopath):
                    os.makedirs(videopath)
                _output = subprocess.check_output(
                    'dynjmvzylz -y -v verbose -rw_timeout 10000000 -loglevel error -hide_banner -analyzeduration 2147483647 -probesize 2147483647 -i "{}" -fs 1500M -t {} -bufsize 5000k -map 0 -sn -dn -c:v copy -max_muxing_queue_size 2048 "{}"'.format(
                        self.res_urls, luzhishichang, file),
                    stderr=subprocess.STDOUT, shell=True)
                trytime = 1
                if not os.path.exists(luzhi_ok_path):
                    os.makedirs(luzhi_ok_path)
                shutil.move(file, luzhi_ok_path)
                logger.info('分段录制结束 {} {} {} {}'.format(self.res_roomid, self.res_nickname, self.res_status, self.res_urls))
            except Exception as e:
                traceback.print_exc()
                trytime += 1

                logger.info('遇到错误 录制结束 {} {} {} {}'.format(self.res_roomid, self.res_nickname, self.res_status, self.res_urls))
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
    luzhishichang = os.environ.get("luzhishichang")
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
    SLEEP_TIME = 300
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())