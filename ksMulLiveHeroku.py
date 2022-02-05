# -*- coding: utf-8 -*-
# @Time    : 2022/1/11 14:41
# @Author  : muyangren907
# @Email   : myr907097904@gmail.com
# @File    : ksMulLiveHeroku.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time    : 2021/8/24 16:23
# @Author  : muyangren907
# @Email   : myr907097904@gmail.com
# @File    : ksMulLive.py
# @Software: PyCharm
import argparse
import base64
import json
import os
import re
import shutil
import sqlite3
import subprocess
# import shutil
import threading
import time
import traceback

import requests


def base64encode(s):
    en = base64.b64encode(s.encode('utf-8'))
    return en.decode('utf-8')


def base64decode(a):
    de = base64.b64decode(a)
    return de.decode('utf-8')


# from multiprocessing import Process, Lock
timeOut = 10

import logging  # 引入logging模块
import os.path

# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级开关
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)


def get_timenow():
    return time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))


# def log_print(strin, end='\n'):
#     print('[ %s ] %s' % (get_timenow(), strin), end=end)


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
        # logger.info('休眠 %5s s' % i)
        print('休眠 %5s s' % i, end='\r')
        time.sleep(1)


def get_database_conn():
    conn = sqlite3.connect('kuaishou.db')
    return conn


def insert_db(id_, eid_, name_, avatar_, principalId_, description_, sex_):
    conn = get_database_conn()
    cursor = conn.cursor()
    # sql = 'INSERT INTO "main"."bilibili"("author_id", "author_nickname", "video_title") VALUES ("{}", "{}", "{}")'.format(
    #     author, author_nickname, video_title)
    sql = 'INSERT OR IGNORE INTO "main"."kuaishou"("id", "eid", "name", "avatar", "principalId", "description", "sex") VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(
        id_, eid_, name_, avatar_, principalId_, description_, sex_)

    cursor.execute(sql)
    # # 关闭Cursor:
    cursor.close()
    # 提交事务:
    conn.commit()
    # 关闭Connection:
    conn.close()


class logThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            logger.info('')
            logger.info('[{}] 正在下载{}个\n'.format(get_timenow(), threading.active_count()))
            logger.info('*' * 10)
            logger.info('共有主播 {}'.format(len(hrids)))
            # for hrid in hrids:
            #     logger.info(hrid)
            logger.info('-' * 10)
            logger.info('-' * 10)
            logger.info('正在下载 {}'.format(len(dlrids)))
            for dlrid in dlrids:
                author_nickname, author_live_url_quality, author_live_url, avatar_, name_ = author_dic[dlrid]
                logger.info('{}_{}'.format(author_nickname, dlrid))
                idx = dlrids.index(dlrid)
                if idx % 3 == 0 or idx % 3 == 1:
                    logger.info('')
                else:
                    logger.info('')
            logger.info('')
            logger.info('*' * 10)

            logger.info('未在直播 {}'.format(len(notlivings)))
            # for notliving in notlivings:
            #     logger.info(notliving, end='')
            #     idx = notlivings.index(notliving)
            #     if idx % 3 == 0 or idx % 3 == 1:
            #         logger.info(end="\t")
            #     else:
            #         logger.info()
            logger.info('')
            logger.info('*' * 10)

            # logger.info('正在合成 {}'.format(len(mergerids)))
            # for mergerid in mergerids:
            #     print(mergerid)
            sleep_dis(10)


class getm3u8Thread(threading.Thread):
    def __init__(self, threadID, threadURL, host, realpath, room, start_time, rid):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadURL = threadURL
        self.host = host
        self.realpath = realpath
        self.room = room
        self.start_time = start_time
        self.rid = rid

    def down_m3u8(self):
        try:
            ffmpeg_path = "ffmpeg"
            file = '{}.mp4'.format(self.room)
            file = os.path.join(record_dir, file)
            _output = subprocess.check_output([
                ffmpeg_path, "-y",
                "-v", "verbose",
                "-rw_timeout", "10000000",  # 10s
                "-loglevel", "error",
                "-hide_banner",
                "-analyzeduration", "2147483647",
                "-probesize", "2147483647",
                "-i", '%s' % self.threadURL,
                "-fs", "800M",
                "-t", "1200",
                '-bufsize', '5000k',
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

            recordfinish = True
            counttime = time.time()
            # if startname in recording:
            #     recording.remove(startname)
            logger.info('{} 直播录制完成'.format(self.room))
            # logger.info('\n' + self.room + " " + time.strftime('%Y-%m-%d %H:%M:%S  ') + '直播录制完成\n')
            if self.rid in dlrids:
                dlrids.remove(self.rid)
            if not os.path.exists(record_ok_pathtmp):
                os.makedirs(record_ok_pathtmp)

            # 直接SSD内部解决

            if os.path.exists(file):
                logger.info('{} --> {} start'.format(file, record_ok_pathtmp))
                # logger.info(file, '-->', record_ok_pathtmp, 'start')
                shutil.move(file, record_ok_pathtmp)
                logger.info('{} --> {} succeed!'.format(file, record_ok_pathtmp))
                # logger.info(file, '-->', record_ok_pathtmp, 'succeed!')

            # record_ok_tmp_file = os.path.join(record_ok_pathtmp, file)
            # # # logger.warning(self.room + " " + "直播录制完成")
            # # if not os.path.exists(record_ok_path):
            # #     os.makedirs(record_ok_path)
            # if os.path.exists(record_ok_tmp_file):
            #     shutil.move(record_ok_tmp_file, record_ok_path)
            #     logger.info('{} --> {} succeed!'.format(record_ok_tmp_file, record_ok_path))
            # logger.info(record_ok_tmp_file, '-->', record_ok_path, 'succeed!')
        except Exception as e:
            traceback.print_exc()
            recordfinish = True
            # if not os.path.exists(record_ok_path):
            #     os.makedirs(record_ok_path)
            # if os.path.exists(file):
            #     shutil.move(file, record_ok_path)
            #     logger.info(file, '-->', record_ok_path, 'succeed!')
            if self.rid in dlrids:
                dlrids.remove(self.rid)
            if not os.path.exists(record_ok_pathtmp):
                os.makedirs(record_ok_pathtmp)
            logger.info('{} {}'.format(self.room, traceback.format_exc()))
            traceback.print_exc()

    def run(self):
        global endFlag
        # print('M3U8获取线程启动 {}'.format(self.threadID))
        # self.get_file_urls(self.threadURL)
        # dlrids.append(self.room)
        self.down_m3u8()
        endFlag = True
        # if self.room in dlrids:
        #     dlrids.remove(self.room)
        # if self.rid in dlrids:
        #     dlrids.remove(self.rid)
        logger.info(str(endFlag))
        # print('endFlag {}'.format(endFlag))
        # print('M3U8获取线程退出 {}'.format(self.threadID))
        return -1


class KuaiShou:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        cookies = {
            'did': 'web_ba32bf2706abc579db6ac28405c3970c',
            'userId': '647446218',
            'kuaishou.live.web_st': 'ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAd4C-es0wDjangqbe_vZzXuTaO0HgB9sB2MDD85iv82otSHSYLev30Hq14AZM6q3N-KcG04K1uirdgPYVo2tDHpWXnXdIZBlKG_BpwW38mauPY2iCRPjj7lFuxC_4opw5nX_0CLb7ERq9PCSYCLTWuYxLW6LIrDYTr_CZxRCkoSITyJ16KeUmD13cHYYbk01pwFoOGf9V0ptM9a3NHKUBjwaEiWGLfbrnUkCqTgL7M-vFrp6OSIgjQmt32ve90PgAvfAzOcBE45X8UrD6O1gQdOFHHKTc9ooBTAB',
        }

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        }
        qualities = ['blueRay', 'super', 'high', 'standard']
        with requests.Session() as s:
            # res = s.get('https://m.gifshow.com/fw/live/{}'.format(self.rid), headers=headers)
            res = s.get('https://live.kuaishou.com/u/{}'.format(self.rid), headers=headers, cookies=cookies)
            # print(res.text)
            livestream = re.search(r'"liveStream":(.*),"feedInfo', res.text)
            livestream = livestream.group(0).replace(',"feedInfo', '')
            livestream = '{%s}' % (livestream)
            # print(livestream)
            livestreamjson = json.loads(livestream)
            try:
                if livestream:
                    livestream = livestreamjson['liveStream']
                    playUrls = livestream['json']['playUrls']
                    # for playUrl in playUrls:
                    #     quality = playUrl['quality']
                    #     url = playUrl['url']
                    #     print(quality, url)
                    playUrl = playUrls[0]
                    quality = playUrl['quality']
                    url = playUrl['url']
                    logger.info(str([quality, url]))
                    return url
                else:
                    raise Exception('直播间不存在或未开播')
            except:
                traceback.print_exc()
                logger.info('{} {}'.format(self.rid, traceback.format_exc()))
                return -1


def get_real_url(rid):
    try:
        ks = KuaiShou(rid)
        return ks.get_real_url()
    except Exception as e:
        traceback.print_exc()
        logger.info('Exception：{}'.format(e))
        return -1


def main(rid):
    global dlrids
    global downEndFlag
    start_time = time.time()

    # logger.info('解析链接中')
    logger.debug('{} 解析链接中'.format(rid))
    # rurl = get_real_url(rid)
    author_nickname, author_live_url_quality, author_live_url, avatar_, name_ = author_dic[rid]
    rurl = author_live_url
    logger.debug('rurl = get_real_url({}) = {}'.format(rid, rurl))
    if rurl == -1:
        return -1
    # logger.info('获取链接成功%s' % rurl)
    logger.debug('{} 获取链接成功{}'.format(rid, rurl))

    # url = 'http://pull-hls-f1.douyincdn.com/stage/stream-394981987741335653/playlist.m3u8'
    chanel_max = len(rurl)
    # for chanel_ in range(chanel_max):
    #     url = rurl[chanel_]
    chanel_ = 0
    # print(rurl)
    url = rurl
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
    try:
        while iiii < iiii_max:
            iiii += 1

            url = rurl
            time_now = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
            # last_split = url.rindex('/')
            #
            # host = url[:last_split]
            author_nickname, author_live_url_quality, author_live_url, avatar_, name_ = author_dic[rid]
            ksnickname = author_nickname
            room = '快手直播_%s_%s_%s_%s' % (LIVE_NAME_PRE, ksnickname, rid, time_now)
            start_time = time.time()
            logger.debug(
                '{} getm3u8Thread(1, {},  {},  {},  {},  {})'.format(rid, url, host, realpath, room, start_time))
            thread_getm3u8 = getm3u8Thread(1, url, host, realpath, room, start_time, rid)
            dlrids = list(set(dlrids))
            if rid not in dlrids:
                dlrids.append(rid)
                dlrids = list(set(dlrids))
            # else:
            #     print('326')
            thread_getm3u8.start()
            thread_getm3u8.join()
            if time.time() - start_time > d_time:
                downEndFlag = True
                # if room in dlrids:
                #     dlrids.remove(room)
                # return
                return -2
            time.sleep(1)

    except Exception as e:
        # logger.info('链接不对劲')
        # logger.info('解析链接中')
        traceback.print_exc()
        logging.error(e)
        if rid in dlrids:
            dlrids.remove(rid)
        downEndFlag = False
        logger.debug('{} {}'.format(rid, traceback.format_exc()))
        traceback.print_exc()
        rurl = get_real_url(rid)
        if rurl == -1:
            # if room in dlrids:
            #     dlrids.remove(room)
            return -1

            # logger.info('获取链接成功%s' % rurl)
        # downflagtrytime += 1
        # if downflagtrytime == downflagtrytimeMAX:
        #     downEndFlag = True

    downEndFlag = True
    # logger.info('休息5秒')

    # if room in dlrids:
    #     dlrids.remove(room)
    # mergevideoer = mergevideoThread(room)
    # mergevideoer.start()


class ksDLThread(threading.Thread):
    def __init__(self, rid):
        threading.Thread.__init__(self)
        self.rid = rid

    def run(self):
        global notlivings
        global dlrids
        trytime = 0
        if self.rid in notlivings:
            notlivings.remove(self.rid)
        ret = main(self.rid)
        if ret != -1:
            logger.info('\nmain({}) ret={}'.format(self.rid, ret))
        else:
            notlivings.append(self.rid)
        # if self.rid in dlrids:
        #     dlrids.remove(self.rid)
        # while True:
        #     trytime += 1
        #     # print('\nstart main({})'.format(self.rid))
        #     # logf = os.path.join('log', '%s.txt' % self.rid)
        #     # with open(logf, mode='a+', encoding='utf-8') as logftxt:
        #     #     logftxt.write('[{}] 第{}次获取信息\n'.format(get_timenow(), trytime))
        #     logger.debug('ksDLThread {} 第{}次获取信息'.format(self.rid, trytime))
        #     try:
        #         if self.rid in notlivings:
        #             notlivings.remove(self.rid)
        #         logger.debug('ret = main({})'.format(self.rid))
        #         ret = main(self.rid)
        #         logger.debug('ret = main({}) = {}'.format(self.rid, ret))
        #         if ret != -1:
        #             print('\nmain({}) ret={}'.format(self.rid, ret))
        #         else:
        #             notlivings.append(self.rid)
        #         if ret != -2:
        #             time.sleep(60)
        #     except Exception as e:
        #         # logging.error(e)
        #         # with open(logf, mode='a+', encoding='utf-8') as logftxt:
        #         #     logftxt.write('[{}] '.format(get_timenow(), trytime))
        #         #     traceback.print_exc(logftxt)
        #         #     logftxt.write('\n')
        #
        #         logger.debug('{} {}'.format(self.rid, traceback.format_exc()))
        #         traceback.print_exc()


def get_rids():
    hridstr = ''
    rids_dic = {}
    with open('ksrids.ini', mode='r', encoding='utf-8') as hridsf:
        hridstr = hridsf.read()
    hrids = [hrid for hrid in hridstr.split('\n') if hrid != '']
    for hrid in hrids:
        rid, nickname = hrid.split(',昵称：')
        if rid not in rids_dic:
            rids_dic[rid] = nickname
    return rids_dic


def getherokuargs(query_type):
    h_url = 'https://myrargs.herokuapp.com/api?query_type={}'.format(query_type)

    trytime = 0
    while True:
        trytime += 1
        try:
            res = requests.get(h_url, timeout=10)
            resjson = res.json()
            logger.info('{}'.format(resjson))
            if resjson['success']:
                ret_str = resjson['data']
                break
            else:
                logger.info('获取参数失败 2秒后再试')
                sleep_dis(2)
        except Exception as e:
            traceback.print_exc()
            time.sleep(5)
    return ret_str


def getcookies():
    # cookiesstr = os.environ.get("cookies")
    cookiesstr = getherokuargs("kscookies")
    cookiesstr = base64decode(cookiesstr)
    keyvals = cookiesstr.split('&&&&')
    cookiesobj = {
    }
    for keyval in keyvals:
        if '&&&' not in keyval:
            continue
        key, val = keyval.split('&&&')
        cookiesobj[key] = val
    return cookiesobj


def getids():
    # cookies = {
    #     'did': 'web_2077198417aebfbbc48949437bff73f5',
    #     'didv': '1631014124364',
    #     'clientid': '3',
    #     'client_key': '65890b29',
    #     'kpn': 'GAME_ZONE',
    #     'userId': '647446218',
    #     'kuaishou.live.bfb1s': '3e261140b0cf7444a0ba411c6f227d88',
    #     'kuaishou.live.web_st': 'ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAUGCOgdSRbrBvdH9aexqvUBMGtvyMWRyAKolIq4SfU6DH_XpL8wrt1Vb8xF0m-CtXJ_JGpig_V3eFjLCwepAP6BKD3iY6Aibl9lIjaf1beWdI_0agIwGIFcy6jlfrGKdL7p97FZaIvxQK2xFvXJ8BDSFQNqdHV3-oZ9tyN48UMY0WfzdJJ9f-KUJZmsOLsO_Qy1pyVxfQou2MB_7fL3mKn0aEgL1c1j1KEeWrOe8x-vTC5n9jyIg-5vfeTnEOhl5b5-mBhpR2J8NOqCdM8dyZkLJD8-M3R0oBTAB',
    #     'kuaishou.live.web_ph': 'de40498a4ecf5070ab1921e381edb81dadc1',
    # }
    cookies = getcookies()
    logger.info("{}".format(cookies))
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    response = requests.get('https://live.kuaishou.com/my-follow/living', headers=headers, cookies=cookies, timeout=10)
    restext = response.text
    # logger.info('{}'.format(restext))
    sposstr = '<script>window.__APOLLO_STATE__='
    eposstr = ';(function(){var'
    spos = restext.index(sposstr) + len(sposstr)
    epos = restext[spos:].index(eposstr)
    resjsonstr = restext[spos:spos + epos]
    # logger.info('{}'.format(resjsonstr))
    # print(resjsonstr)
    resjson = json.loads(resjsonstr)
    clients = resjson['clients']
    graphqlServerClient = clients['graphqlServerClient']
    author_dic = {}
    author_ids = []
    for iii in graphqlServerClient:
        if 'LiveInfo' in iii and '.playUrls' not in iii and '.gameInfo' not in iii:
            logger.info(iii)
            iii_obj = graphqlServerClient[iii]
            iii_obj_user_obj_id = iii_obj['user']['id']
            iii_obj_user_obj = graphqlServerClient[iii_obj_user_obj_id]
            author_id = iii_obj_user_obj['id']
            author_nickname = strfomat(iii_obj_user_obj['name'])
            author_live_url_obj = graphqlServerClient['{}.playUrls.0'.format(iii)]
            author_live_url = author_live_url_obj['url']
            author_live_url_quality = author_live_url_obj['quality']

            gameInfo_str = '${}.gameInfo'.format(iii)
            gameInfo_obj = graphqlServerClient[gameInfo_str]
            gameInfo_name = gameInfo_obj['name']
            if gameInfo_name != '购物':
                logger.info('{} 跳过'.format(author_nickname))
                continue
            else:
                logger.info('{} 加入'.format(author_nickname))
            # id_, eid_, name_, avatar_, principalId_, description_, sex_
            id_ = author_id
            avatar_ = iii_obj_user_obj['avatar']
            name_ = iii_obj_user_obj['name']

            logger.info('{} {} {} {}\n'.format(author_id, author_nickname, author_live_url_quality, author_live_url))
            author_dic[author_id] = [author_nickname, author_live_url_quality, author_live_url, avatar_, name_]
            author_ids.append(author_id)
    author_ids = sorted(author_ids)
    author_id_len = len(author_ids)
    ksmullive_idx = int(os.environ.get("ksmullive_idx"))
    ksmullive_tot_str = getherokuargs('ksmullive_tot')
    ksmullive_tot = int(ksmullive_tot_str)
    split_len = author_id_len // ksmullive_tot
    author_id_start = split_len * (ksmullive_idx - 1)
    author_id_end = split_len * ksmullive_idx
    if ksmullive_idx == ksmullive_tot:
        author_id_end = author_id_len
    author_ids_fin = author_ids[author_id_start:author_id_end]
    author_dic_tmp = {}
    for author_id_fin in author_ids_fin:
        author_dic_tmp[author_id_fin] = author_dic[author_id_fin]
    return author_dic_tmp


def strfomat(str_in):
    sub_str = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", str_in)
    return sub_str


if __name__ == '__main__':
    LIVE_NAME_PRE = 'KuaiShou_Kwai'
    # record_ok_pathtmp = '/home/muyangren907/2t/zhiboluzhi/kuaishou/record'
    # record_ok_path = '/home/muyangren907/2t/zhiboluzhi/recordok'
    record_dir = 'record'
    if not os.path.exists(record_dir):
        os.makedirs(record_dir)
    # SSD内部解决
    record_ok_pathtmp = 'recordok'
    record_ok_path = record_ok_pathtmp
    debugmode = False
    # download threads
    dlrids = []
    # merge threads
    mergerids = []
    # 总共hrids
    hrids = []
    notlivings = []

    d_time = 1200
    LOOP_IDX = 0
    downEndFlag = True
    # rid = input('输入虎牙直播房间号：\n')
    logthread = logThread()
    logthread.start()
    while True:

        try:
            logger.info('获取直播列表')
            author_dic = getids()
            logger.info('{}'.format(author_dic))
            logger.info('更新主播信息')
            for author_id in author_dic:
                author_list = author_dic[author_id]
                # id_, eid_, name_, avatar_, principalId_, description_, sex_
                # [author_nickname, author_live_url_quality, author_live_url, avatar_, name_]
                id_ = author_id
                eid_ = ''
                name_ = author_list[0]
                avatar_ = author_list[-2]
                principalId_ = ''
                description_ = ''
                sex_ = ''
                # insert_db(id_, eid_, name_, avatar_, principalId_, description_, sex_)
        except:
            traceback.print_exc()
            sleep_dis(100)
            continue
        # rids_dic = get_rids()
        hridstmp = [rid for rid in author_dic]
        # hridstmp2 = list(set(hrids + hridstmp))
        # hridstmp3 = list(set(hridstmp2) - set(hrids))
        for rid_ in hridstmp:
            if rid_ not in dlrids:
                ksdlthread = ksDLThread(rid_)
                ksdlthread.start()
                dlrids.append(rid_)
                sleep_dis(1)

        # if len(hridstmp3) > 0:
        #     for hrid in hridstmp3:
        #         ksdlthread = ksDLThread(hrid)
        #         ksdlthread.start()
        #         hrids.append(hrid)
        #         sleep_dis(1)
        sleep_dis(100)
