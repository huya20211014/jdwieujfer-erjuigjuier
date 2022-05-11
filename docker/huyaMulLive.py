# -*- coding: utf-8 -*-
# @Time    : 2020/5/29 12:51
# @Author  : muyangren907
# @Email   : myr907097904@gmail.com
# @File    : huyaLive_luzhi.py
# @Software: PyCharm
# 虎牙直播录制脚本
import argparse
import os
import shutil
import subprocess
# import shutil
import threading
import traceback
import configparser

# from multiprocessing import Process, Lock
timeOut = 10

import logging  # 引入logging模块
import os.path

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

def get_timenow():
    return time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))


def log_print(strin, end='\n'):
    print('[ %s ] %s' % (get_timenow(), strin), end=end)


parser = argparse.ArgumentParser()
parser.add_argument('--url', type=str, default=None,
                    help='m3u8 url')
parser.add_argument('--l', type=bool, default=False,
                    help='if loop')
FLAGS = parser.parse_args()
URL = FLAGS.url
LOOP_F = FLAGS.l

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def sleep_dis(sleep_time):
    for i in range(sleep_time, -1, -1):
        print('休眠 %5s s' % i, end='\r')
        time.sleep(1)


class logThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            print()
            logger.info('活跃线程数 {} 录制范围[ {} , {} ]\n'.format(threading.active_count(),luzhi_range[0],luzhi_range[1]))
            print('*' * 10)
            logger.info('共有主播 {}'.format(len(hrids)))
            # for hrid in hrids:
            #     log_print(hrid)
            print('-' * 10)
            print('-' * 10)
            logger.info('正在录制 {} 个'.format(len(dlrids)))
            logstr = ''
            # for dlrid in dlrids:
            #     print(dlrid, end='')
            #     logstr+='{}'.format(dlrid)
            #     idx = dlrids.index(dlrid)
            #     if idx % 3 == 0 or idx % 3 == 1:
            #         logstr+='\t'
            #         print(end="\t")
            #     else:
            #         logstr+='\n'
            #         print()
            # print()
            # print('*' * 10)
            logstr+='*' * 10+'\n'
            logger.info(logstr)
            logstr = ''
            log_print('未在直播 {} 个'.format(len(notlivings)))
            # for notliving in notlivings:
            #     print(notliving, end='')
            #     logstr+=notliving
            #     idx = notlivings.index(notliving)
            #     if idx % 3 == 0 or idx % 3 == 1:
            #         logstr+='\t'
            #         print(end="\t")
            #     else:
            #         logstr+='\n'
            #         print()
            # print()
            # print('*' * 10)
            logstr+='*' * 10+'\n'
            logger.info(logstr)

            # log_print('正在合成 {}'.format(len(mergerids)))
            # for mergerid in mergerids:
            #     print(mergerid)
            time.sleep(5)


class getm3u8Thread(threading.Thread):
    def __init__(self, threadID, threadURL, host, realpath, room, start_time):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadURL = threadURL
        self.host = host
        self.realpath = realpath
        self.room = room
        self.start_time = start_time

    def down_m3u8(self):
        try:
            ffmpeg_path = "ffmpeg"
            file = '{}.mp4'.format(self.room)
            _output = subprocess.check_output([
                ffmpeg_path, "-y",
                "-v", "verbose",
                "-rw_timeout", "10000000",  # 10s
                "-loglevel", "error",
                "-hide_banner",
                "-analyzeduration", "2147483647",
                "-probesize", "2147483647",
                "-i", '%s' % self.threadURL,
                "-fs", "1500M",
                "-t", "1800",
                '-bufsize', '50000k',
                "-map", "0",
                "-sn", "-dn",
                # "-f","mpegts",
                # "-bsf:v","h264_mp4toannexb",
                # "-c","copy",
                # "-c:v","libx264",   #后期可以用crf来控制大小
                "-c:v", "copy",  # 直接用copy的话体积特别大.
                # "-fs",limit_file_size,
                '-max_muxing_queue_size', '2048',
                "{path}".format(path=file),
            ], stderr=subprocess.STDOUT)

            luzhifinish = True
            counttime = time.time()
            # if startname in luzhiing:
            #     luzhiing.remove(startname)
            print('\n' + self.room + " " + time.strftime('%Y-%m-%d %H:%M:%S  ') + '直播录制完成\n')
            # logger.warning(self.room + " " + "直播录制完成")
            if not os.path.exists(luzhi_ok_path):
                os.makedirs(luzhi_ok_path)
            if os.path.exists(file):
                shutil.move(file, luzhi_ok_path)
                print(file, '-->', luzhi_ok_path, 'succeed!')
        except Exception as e:
            luzhifinish = True
            if not os.path.exists(luzhi_ok_path):
                os.makedirs(luzhi_ok_path)
            if os.path.exists(file):
                shutil.move(file, luzhi_ok_path)
                print(file, '-->', luzhi_ok_path, 'succeed!')
            logger.info('{} {}'.format(self.room, traceback.format_exc()))
            traceback.print_exc()

    def run(self):
        global endFlag
        # print('M3U8获取线程启动 {}'.format(self.threadID))
        # self.get_file_urls(self.threadURL)
        try:
            dlrids.append(self.room)
            self.down_m3u8()
            endFlag = True
            if self.room in dlrids:
                dlrids.remove(self.room)
            print(endFlag)
        except Exception as e:
            traceback.print_exc()
            if self.room in dlrids:
                dlrids.remove(self.room)
        # print('endFlag {}'.format(endFlag))
        # print('M3U8获取线程退出 {}'.format(self.threadID))
        return -1


# 获取虎牙直播的真实流媒体地址。
# 虎牙"一起看"频道的直播间可能会卡顿，尝试将返回地址 tx.hls.huya.com 中的 tx 改为 bd、migu-bd。

import requests
import re
import base64
import urllib.parse
import hashlib
import time
import json


class HuYa:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        try:
            livelineurls = []
            room_url = 'https://m.huya.com/' + str(self.rid)
            header = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36 '
            }
            logger.debug('requests.get(url={}, headers=header, timeout=10).text'.format(room_url))
            response = requests.get(url=room_url, headers=header, timeout=10).text
            logger.debug('ok requests.get(url={}, headers=header, timeout=10).text'.format(room_url))

            spos = response.index('window.HNF_GLOBAL_INIT = ') + len('window.HNF_GLOBAL_INIT = ')
            epos = response[spos:].index(' </script>')
            # print(spos,epos)
            jsonstr = response[spos:spos + epos]
            # print(jsonstr)
            jsonobj = json.loads(jsonstr)

            roomInfo = jsonobj['roomInfo']
            # print(roomInfo)
            tProfileInfo = roomInfo['tProfileInfo']
            '''
            "tProfileInfo": {
            "lUid": 1615255773,
            "lYyid": 1829444918,
            "sNick": "赢城-陈莫沫【566】",
            "iSex": 2,
            "iLevel": 36,
            "sAvatar180": "https://huyaimg.msstatic.com/avatar/1080/81/c2fd41e3369ec54e08648d6cf5400e_180_135.jpg?1618510507",
            "lProfileRoom": 56620,
            "sPrivateHost": "1829444918",
            "lActivityId": 0,
            "lActivityCount": 758290,
            "_classname": "LiveRoom.LiveProfileInfo"
            },
            '''

            tLiveInfo = roomInfo['tLiveInfo']
            tLiveStreamInfo = tLiveInfo['tLiveStreamInfo']
            vStreamInfo = tLiveStreamInfo['vStreamInfo']
            values = vStreamInfo['value']
            for value in values:
                '''
                "sFlvUrl": "http://al.flv.huya.com/src",
"sFlvUrlSuffix": "flv",
"sFlvAntiCode": "wsSecret=1cd73802738d52a349ea2a4e33079a66&wsTime=60d735a3&fm=RFdxOEJjSjNoNkRKdDZUWV8kMF8kMV8kMl8kMw%3D%3D&ctype=tars_mobile&txyp=o%3Aw2%3B&fs=bgct&&sphdcdn=al_7-tx_3-js_3-ws_7-bd_2-hw_2&sphdDC=huya&sphd=264_*-265_*&t=103",
"sHlsUrl": "http://al.hls.huya.com/src",
"sHlsUrlSuffix": "m3u8",
"sHlsAntiCode": "wsSecret=1cd73802738d52a349ea2a4e33079a66&wsTime=60d735a3&fm=RFdxOEJjSjNoNkRKdDZUWV8kMF8kMV8kMl8kMw%3D%3D&ctype=tars_mobile&txyp=o%3Aw2%3B&fs=bgct&&sphdcdn=al_7-tx_3-js_3-ws_7-bd_2-hw_2&sphdDC=huya&sphd=264_*-265_*&t=103",
                '''
                sHlsUrl = value['sHlsUrl']
                sFlvUrl = value['sFlvUrl']
                sHlsUrlSuffix = value['sHlsUrlSuffix']
                sFlvUrlSuffix = value['sFlvUrlSuffix']
                sHlsAntiCode = value['sHlsAntiCode']
                sFlvAntiCode = value['sFlvAntiCode']
                sStreamName = value['sStreamName']
                # liveurl = '{}/{}.{}?{}'.format(sHlsUrl, sStreamName, sHlsUrlSuffix, sHlsAntiCode)
                liveurl = '{}/{}.{}?{}'.format(sFlvUrl, sStreamName, sFlvUrlSuffix, sFlvAntiCode)
                # print(liveurl)
                livelineurls.append(liveurl)

            # livelineurls = re.findall(r'liveLineUrl = "([\s\S]*?)";', response)
            if debugmode:
                print(livelineurls)
            logger.debug('{} livelineurls  {}'.format(self.rid, livelineurls))
            # livelineurl = livelineurls[0]
            # # print(livelineurl)
            # livelineurl = str(base64.b64decode(livelineurl), encoding="utf-8")
            # # print(livelineurl)
            # if livelineurl:
            #     if 'replay' in livelineurl:
            #         real_url = {
            #             'replay': "https:" + livelineurl,
            #         }
            #     else:
            #         s_url = self.live(livelineurl)
            #         b_url = self.live(livelineurl.replace('_2000', ''))
            #         real_url = {
            #             '2000p': "https:" + s_url,
            #             'tx': "https:" + b_url,
            #             'bd': "https:" + b_url.replace('tx.hls.huya.com', 'bd.hls.huya.com'),
            #             'migu-bd': "https:" + b_url.replace('tx.hls.huya.com', 'migu-bd.hls.huya.com'),
            #         }
            if len(livelineurls) > 0:
                real_url = livelineurls
            else:
                # raise Exception('未开播或直播间不存在')
                if debugmode:
                    log_print('未开播或直播间不存在')
                logger.debug('{} 未开播或直播间不存在'.format(self.rid))
                return -1
        except Exception as e:
            # raise Exception('未开播或直播间不存在')
            logger.debug('{} 未开播或直播间不存在'.format(self.rid))
            logging.debug(traceback.format_exc())
            if debugmode:
                log_print(e)
                log_print('未开播或直播间不存在')
            return -1
        return real_url

    @staticmethod
    def live(e):
        i, b = e.split('?')
        r = i.split('/')
        s = re.sub(r'.(flv|m3u8)', '', r[-1])
        c = b.split('&', 3)
        c = [i for i in c if i != '']
        n = {i.split('=')[0]: i.split('=')[1] for i in c}
        fm = urllib.parse.unquote(n['fm'])
        u = base64.b64decode(fm).decode('utf-8')
        p = u.split('_')[0]
        f = str(int(time.time() * 1e7))
        ll = n['wsTime']
        t = '0'
        h = '_'.join([p, t, s, f, ll])
        m = hashlib.md5(h.encode('utf-8')).hexdigest()
        y = c[-1]
        url = "{}?wsSecret={}&wsTime={}&u={}&seqid={}&{}".format(i, m, ll, t, f, y)
        return url


def get_real_url(rid):
    try:
        hy = HuYa(rid)
        real_url = hy.get_real_url()
        return real_url
    except Exception as e:
        print('Exception：', e)
        logging.error(traceback.format_exc())
        return -1


def main(rid):
    global dlrids
    global downEndFlag
    start_time = time.time()

    # log_print('解析链接中')
    logger.debug('{} 解析链接中'.format(rid))
    rurl = get_real_url(rid)
    logger.debug('rurl = get_real_url({}) = {}'.format(rid, rurl))
    if rurl == -1:
        return -1
    # log_print('获取链接成功%s' % rurl)
    logger.debug('{} 获取链接成功{}'.format(rid, rurl))

    # url = 'http://pull-hls-f1.douyincdn.com/stage/stream-394981987741335653/playlist.m3u8'
    chanel_max = len(rurl)
    # for chanel_ in range(chanel_max):
    #     url = rurl[chanel_]
    chanel_ = 0
    # print(rurl)
    url = rurl[chanel_]
    if url is None:
        url = input('请输入url:\n')

    # lock = threading.Lock()
    m3u8s_g = []
    endFlag = False

    time_now = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    last_split = url.rindex('/')

    host = url[:last_split]
    room = '%s_%s' % (rid, time_now)
    # print(room)
    # room_dir = os.path.join(BASE_DIR, room)
    # if not os.path.exists(room_dir):
    #     os.makedirs(room_dir)
    realpath = os.path.dirname(os.path.realpath('__file__'))
    downflag = True
    rurlo = ''
    downflagtrytime = 0
    downflagtrytimeMAX = 2
    iiii = 0
    iiii_max = 2
    while iiii < iiii_max:
        iiii += 1
        try:
            url = rurl[chanel_]
            time_now = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
            last_split = url.rindex('/')

            host = url[:last_split]
            room = '%s_%s' % (rid, time_now)
            start_time = time.time()
            logger.debug(
                '{} getm3u8Thread(1, {},  {},  {},  {},  {})'.format(rid, url, host, realpath, room, start_time))
            thread_getm3u8 = getm3u8Thread(1, url, host, realpath, room, start_time)

            thread_getm3u8.start()
            thread_getm3u8.join()
            if time.time() - start_time > d_time:
                downEndFlag = True
                # if room in dlrids:
                #     dlrids.remove(room)
                # return
                return -2
            else:
                # if room in dlrids:
                #     dlrids.remove(room)
                chanel_ = (chanel_ + 1) % chanel_max
                print('{} 切换通道 {}'.format(rid, chanel_))
        except Exception as e:
            # log_print('链接不对劲')
            # log_print('解析链接中')
            logging.error(e)
            downEndFlag = False
            logger.debug('{} {}'.format(rid, traceback.format_exc()))
            traceback.print_exc()
            rurl = get_real_url(rid)
            if rurl == -1:
                # if room in dlrids:
                #     dlrids.remove(room)
                return -1
            else:
                chanel_ = (chanel_ + 1) % chanel_max
                print('{} 切换通道 {}'.format(rid, chanel_))
            # log_print('获取链接成功%s' % rurl)
        downflagtrytime += 1
        if downflagtrytime == downflagtrytimeMAX:
            downEndFlag = True
            break
        downEndFlag = True
        # log_print('休息5秒')
        time.sleep(1)
        # if room in dlrids:
        #     dlrids.remove(room)
    # mergevideoer = mergevideoThread(room)
    # mergevideoer.start()


class huyaDLThread(threading.Thread):
    def __init__(self, rid):
        threading.Thread.__init__(self)
        self.rid = rid

    def run(self):
        global notlivings
        trytime = 0
        while True:
            trytime += 1
            # print('\nstart main({})'.format(self.rid))
            # logf = os.path.join('log', '%s.txt' % self.rid)
            # with open(logf, mode='a+', encoding='utf-8') as logftxt:
            #     logftxt.write('[{}] 第{}次获取信息\n'.format(get_timenow(), trytime))
            logger.debug('huyaDLThread {} 第{}次获取信息'.format(self.rid, trytime))
            try:
                if self.rid in notlivings:
                    notlivings.remove(self.rid)
                logger.debug('ret = main({})'.format(self.rid))
                ret = main(self.rid)
                logger.debug('ret = main({}) = {}'.format(self.rid, ret))
                if ret != -1:
                    print('\nmain({}) ret={}'.format(self.rid, ret))
                else:
                    notlivings.append(self.rid)
                if ret != -2:
                    time.sleep(60)
            except Exception as e:
                # logging.error(e)
                # with open(logf, mode='a+', encoding='utf-8') as logftxt:
                #     logftxt.write('[{}] '.format(get_timenow(), trytime))
                #     traceback.print_exc(logftxt)
                #     logftxt.write('\n')

                logger.debug('{} {}'.format(self.rid, traceback.format_exc()))
                traceback.print_exc()

def get_config():
    config = configparser.ConfigParser()
    # -read读取ini文件
    config.read('config.ini', encoding='utf-8-sig')
    if '1' not in config.sections():
        config.add_section('1')
    return config['1']

def get_rids():
    global luzhi_range
    config = get_config()
    rangeidx = int(config['rangeidx'])
    rangebase = int(config['rangebase'])
    hridstr = ''
    with open('huyarids.ini', mode='r', encoding='utf-8') as hridsf:
        hridstr = hridsf.read()
    startidx = rangeidx*rangebase
    endidx = (rangeidx+1)*rangebase
    hridstrsp = [hrid for hrid in hridstr.split('\n') if hrid != '']
    if endidx>=len(hridstrsp):
        endidx=len(hridstrsp)-1
    hrids = list(set(hridstrsp[startidx:endidx]))
    luzhi_range = [startidx,endidx]
    return hrids


if __name__ == '__main__':
    luzhi_ok_path = 'luzhichenggong'
    luzhi_range = [0,0]
    debugmode = False
    # download threads
    dlrids = []
    # merge threads
    mergerids = []
    # 总共hrids
    hrids = []
    notlivings = []

    d_time = 1800
    LOOP_IDX = 0
    downEndFlag = True
    # rid = input('输入虎牙直播房间号：\n')
    logger.info("logger 线程开启")
    logthread = logThread()
    logthread.start()
    while True:
        hridstmp = get_rids()
        hridstmp2 = list(set(hrids + hridstmp))
        hridstmp3 = list(set(hridstmp2) - set(hrids))
        if len(hridstmp3) > 0:
            for hrid in hridstmp3:
                huyadlthread = huyaDLThread(hrid)
                huyadlthread.start()
                hrids.append(hrid)
                sleep_dis(1)
        sleep_dis(5)