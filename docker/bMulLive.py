# -*- coding: utf-8 -*-
# @Time    : 2021/12/19 23:53
# @Author  : muyangren907
# @Email   : myr907097904@gmail.com
# @File    : blive.py
# @Software: PyCharm
import argparse
import configparser
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

def urlencode(text):
    from urllib.parse import unquote
    text = unquote(text, 'utf-8')
    return text

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
        print('休眠 %5s s' % i, end='\r')
        time.sleep(1)


def get_database_conn():
    conn = sqlite3.connect('bllive.db')
    return conn


def insert_db(id_, name_, name_now):
    conn = get_database_conn()
    cursor = conn.cursor()
    # sql = 'INSERT INTO "main"."bilibili"("author_id", "author_nickname", "video_title") VALUES ("{}", "{}", "{}")'.format(
    #     author, author_nickname, video_title)
    sql = 'INSERT OR IGNORE INTO "main"."bilibili"("id", "nickname", "nickname_now") VALUES ("{}", "{}", "{}")'.format(
        id_, name_, name_now)

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
        global dlrids
        global notlivings
        while True:
            print()
            thactivates = threading.enumerate()
            logger.info('[{}] 活跃线程数 {} 个\n{}'.format(get_timenow(), threading.active_count(), thactivates))
            if len(author_dic) == 0:
                logger.info('author_dic 初始化未完成')
                sleep_dis(10)
                continue
            dlridstmp = []
            for thactivate in thactivates:
                logger.info('{}'.format(thactivate))
                th_rid = thactivate.name.split('-')[0]
                if 'Thread' in th_rid:
                    continue
                if th_rid not in dlridstmp:
                    dlridstmp.append(th_rid)
            dlrids = dlridstmp
            notlivingstmp = []
            for iiid in author_dic:
                if iiid not in dlrids:
                    notlivingstmp.append(iiid)
            notlivings = notlivingstmp
            print('*' * 10)
            logger.info('共有主播 {}'.format(len(author_dic)))
            print()

            print('-' * 10)
            logger.info('正在下载 {}'.format(len(dlrids)))
            for dlrid in dlrids:
                # author_nickname, author_live_url_quality, author_live_url, avatar_, name_ = author_dic[dlrid]
                author_nickname, nickname_now = author_dic[dlrid]
                print('{}_{}'.format(author_nickname, dlrid), end='')
                idx = dlrids.index(dlrid)
                if idx % 3 == 0 or idx % 3 == 1:
                    print(end="\t")
                else:
                    print()
            print()
            print('*' * 10)

            logger.info('未在直播 {}'.format(len(notlivings)))
            for notliving in notlivings:
                author_nickname, nickname_now = author_dic[notliving]
                print('{}_{}'.format(author_nickname, notliving), end='')
                idx = notlivings.index(notliving)
                if idx % 3 == 0 or idx % 3 == 1:
                    print(end="\t")
                else:
                    print()
            print()
            print('*' * 10)

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
        try_max = 3
        try_time = 0
        self.nickname = author_dic[self.rid][0]
        while try_time < try_max:
            try:
                try_time += 1
                logger.info('{}-{} 尝试 [{} / {}] 次 录制'.format(self.rid, self.nickname, try_time, try_max))
                ffmpeg_path = "ffmpeg"
                file = '{}.mp4'.format(self.room)
                file = os.path.join(record_dir, file)
                # self.threadURL = 'http://{}'.format(urlencode(self.threadURL.replace('https://', '').replace('http://', '')))
                # _output = subprocess.check_output([
                #     ffmpeg_path, "-y",
                #     "-v", "verbose",
                #     "-rw_timeout", "10000000",  # 10s
                #     "-loglevel", "error",
                #     "-hide_banner",
                #     "-analyzeduration", "2147483647",
                #     "-probesize", "2147483647",
                #     "-i", self.threadURL,
                #     "-fs", "1500M",
                #     "-t", "1800",
                #     '-bufsize', '5000k',
                #     "-map", "0",
                #     "-sn", "-dn",
                #     # "-f","mpegts",
                #     # "-bsf:v","h264_mp4toannexb",
                #     # "-c","copy",
                #     # "-c:v","libx264",   #后期可以用crf来控制大小
                #     "-c:v", "copy",  # 直接用copy的话体积特别大.
                #     # "-fs",limit_file_size,
                #     '-max_muxing_queue_size', '2048',
                #     "{path}".format(path=file),
                # ], stderr=subprocess.STDOUT)
                luzhishichang = os.environ.get("luzhishichang")
                _output = subprocess.check_output(
                    'ffmpeg -y -v verbose -rw_timeout 10000000 -loglevel error -hide_banner -analyzeduration 2147483647 -probesize 2147483647 -i "{}" -fs 1500M -t {} -bufsize 5000k -map 0 -sn -dn -c:v copy -max_muxing_queue_size 2048 "{}"'.format(self.threadURL,luzhishichang,file),
                    stderr=subprocess.STDOUT, shell=True)

                recordfinish = True
                counttime = time.time()
                # if startname in recording:
                #     recording.remove(startname)
                logger.info('{} 直播录制完成'.format(self.room))
                # logger.info('\n' + self.room + " " + time.strftime('%Y-%m-%d %H:%M:%S  ') + '直播录制完成\n')
                # if self.rid in dlrids:
                #     dlrids.remove(self.rid)
                if not os.path.exists(record_ok_pathtmp):
                    os.makedirs(record_ok_pathtmp)

                # 直接SSD内部解决

                if os.path.exists(file):
                    logger.info('{} --> {} start'.format(file, record_ok_pathtmp))
                    # logger.info(file, '-->', record_ok_pathtmp, 'start')
                    shutil.move(file, record_ok_pathtmp)
                    logger.info('{} --> {} succeed!'.format(file, record_ok_pathtmp))
                    # logger.info(file, '-->', record_ok_pathtmp, 'succeed!')
                break
                # record_ok_tmp_file = os.path.join(record_ok_pathtmp, file)
                # # # logger.warning(self.room + " " + "直播录制完成")
                # # if not os.path.exists(record_ok_path):
                # #     os.makedirs(record_ok_path)
                # if os.path.exists(record_ok_tmp_file):
                #     shutil.move(record_ok_tmp_file, record_ok_path)
                #     logger.info('{} --> {} succeed!'.format(record_ok_tmp_file, record_ok_path))
                # logger.info(record_ok_tmp_file, '-->', record_ok_path, 'succeed!')
            except Exception as e:
                recordfinish = True
                # if not os.path.exists(record_ok_path):
                #     os.makedirs(record_ok_path)
                # if os.path.exists(file):
                #     shutil.move(file, record_ok_path)
                #     logger.info(file, '-->', record_ok_path, 'succeed!')
                # if self.rid in dlrids:
                #     dlrids.remove(self.rid)
                if not os.path.exists(record_ok_pathtmp):
                    os.makedirs(record_ok_pathtmp)
                logger.info('{} {}'.format(self.room, traceback.format_exc()))
                traceback.print_exc()
                slpt = 3
                logger.info('{}录制异常 {}秒后重试'.format(self.room, slpt))
                time.sleep(slpt)

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


class BiliBili:

    def __init__(self, rid):
        """
        有些地址无法在PotPlayer播放，建议换个播放器试试
        Args:
            rid:
        """
        rid = rid
        self.rid = rid
        self.header = {
            'User-Agent': 'Mozilla/5.0 (iPod; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                          'like Gecko) CriOS/87.0.4280.163 Mobile/15E148 Safari/604.1',
        }
        # 先获取直播状态和真实房间号
        r_url = 'https://api.live.bilibili.com/room/v1/Room/room_init'
        param = {
            'id': rid
        }
        try_time = 0
        try_max = 3
        while try_time < try_max:
            try:
                try_time += 1
                logger.info('{}-{} {}/{} 次 room_init'.format(self.rid, author_dic[self.rid][0], try_time, try_max))
                with requests.Session() as self.s:
                    if len(proxies2) > 0:
                        res = self.s.get(r_url, headers=self.header, params=param, proxies=proxies2, timeout=10).json()
                    else:
                        res = self.s.get(r_url, headers=self.header, params=param, timeout=10).json()
                break
            except Exception as e:
                traceback.print_exc()
                slpt = 3
                logger.info('room_init失败 {}秒后重试'.format(slpt))
                sleep_dis(slpt)
        if res['msg'] == '直播间不存在':
            raise Exception(f'bilibili {rid} {res["msg"]}')
        # print(res)
        live_status = res['data']['live_status']
        self.real_room_id = res['data']['room_id']
        if live_status != 1:
            # raise Exception(f'bilibili {rid} 未开播')
            self.real_room_id = -1

    def get_real_url(self, current_qn: int = 10000):
        if self.real_room_id == -1:
            return -1
        try_time = 0
        try_max = 3
        while try_time < try_max:
            try:
                try_time += 1
                logger.info(
                    '{}-{} {}/{} 次 getRoomPlayInfo'.format(self.rid, author_dic[self.rid][0], try_time, try_max))
                url = 'https://api.live.bilibili.com/xlive/web-room/v2/index/getRoomPlayInfo'
                param = {
                    'room_id': self.real_room_id,
                    'protocol': '0,1',
                    'format': '0,1,2',
                    'codec': '0,1',
                    'qn': current_qn,
                    'platform': 'h5',
                    'ptype': 8,
                }
                if len(proxies2) > 0:
                    res = self.s.get(url, headers=self.header, params=param, proxies=proxies2, timeout=10)
                else:
                    res = self.s.get(url, headers=self.header, params=param, timeout=10)
                break
            except Exception as e:
                traceback.print_exc()
                slpt = 3
                logger.info('getRoomPlayInfo失败 {}秒后重试'.format(slpt))
                sleep_dis(slpt)

        # print(res.text)
        res = res.json()
        # print(res)
        stream_info = res['data']['playurl_info']['playurl']['stream']
        qn_max = 0

        for data in stream_info:
            accept_qn = data['format'][0]['codec'][0]['accept_qn']
            for qn in accept_qn:
                qn_max = qn if qn > qn_max else qn_max
        if qn_max != current_qn:
            param['qn'] = qn_max
            res = self.s.get(url, headers=self.header, params=param).json()
            stream_info = res['data']['playurl_info']['playurl']['stream']

        stream_urls = {}
        # flv流无法播放，暂修改成获取hls格式的流，
        for data in stream_info:
            format_name = data['format'][0]['format_name']
            if format_name == 'ts':
                base_url = data['format'][-1]['codec'][0]['base_url']
                url_info = data['format'][-1]['codec'][0]['url_info']
                for i, info in enumerate(url_info):
                    host = info['host']
                    extra = info['extra']
                    # stream_urls[f'线路{i + 1}'] = f'{host}{base_url}{extra}'
                    stream_urls[i] = f'{host}{base_url}{extra}'
                break
        return stream_urls[0]


def get_real_url(rid):
    try:
        bl = BiliBili(rid)
        ru = bl.get_real_url()
        return ru
    except Exception as e:
        traceback.print_exc()
        return -1


def main(rid):
    global dlrids
    global downEndFlag
    start_time = time.time()

    # logger.info('解析链接中')
    logger.info('{} 解析链接中'.format(rid))
    rurl = get_real_url(rid)
    author_nickname, nickname_now = author_dic[rid]
    # rurl = author_live_url
    logger.info('rurl = get_real_url({}) = {}'.format(rid, rurl))
    if rurl == -1:
        return -1
    # logger.info('获取链接成功%s' % rurl)
    logger.info('{} 获取链接成功{}'.format(rid, rurl))

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
    # try:
    while iiii < iiii_max:
        try:
            iiii += 1

            url = rurl
            time_now = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
            # last_split = url.rindex('/')
            #
            # host = url[:last_split]
            author_nickname, nickname_now = author_dic[rid]
            ksnickname = author_nickname
            room = 'B站直播_%s_%s_%s' % (ksnickname, rid, time_now)
            start_time = time.time()
            logger.info(
                '{} getm3u8Thread(1, {},  {},  {},  {},  {})'.format(rid, url, host, realpath, room, start_time))
            thread_getm3u8 = getm3u8Thread(1, url, host, realpath, room, start_time, rid)
            thread_getm3u8.name = '{}-{}-{}'.format(rid, ksnickname, get_timenow())
            dlrids = list(set(dlrids))

            # else:
            #     print('326')
            thread_getm3u8.start()
            thread_getm3u8.join()
            if time.time() - start_time > d_time:
                downEndFlag = True
                # if rid in dlrids:
                #     logger.info('dlrids.remove({})'.format(rid))
                #     dlrids.remove(rid)
                # return
                return -2
            break
            # time.sleep(1)

        except Exception as e:
            # logger.info('链接不对劲')
            # logger.info('解析链接中')
            logging.error(e)
            # if rid in dlrids:
            #     logger.info('dlrids.remove({})'.format(rid))
            #     dlrids.remove(rid)
            downEndFlag = False
            logger.info('{} {}'.format(rid, traceback.format_exc()))
            traceback.print_exc()
            # rurl = get_real_url(rid)
            # if rurl == -1:
            #     # if room in dlrids:
            #     #     dlrids.remove(room)
            #     return -1
            sleep_dis(3)

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
        # if self.rid not in dlrids:
        #     dlrids.append(self.rid)
        #     dlrids = list(set(dlrids))
        #     logger.info('dlrids.append({})'.format(self.rid))
        # if self.rid in notlivings:
        #     notlivings.remove(self.rid)
        ret = main(self.rid)
        if ret != -1:
            print('\nmain({}) ret={}'.format(self.rid, ret))
        else:
            pass
            # if self.rid in dlrids:
            #     logger.info('dlrids.remove({})'.format(self.rid))
            #     dlrids.remove(self.rid)
            # notlivings.append(self.rid)


def get_rids():
    hridstr = ''
    rids_dic = {}
    # with open('blrids.ini', mode='r', encoding='utf-8') as hridsf:
    #     hridstr = hridsf.read()
    # hrids = [hrid for hrid in hridstr.split('\n') if hrid != '']
    # for hrid in hrids:
    #     rid, nickname = hrid.split(' ')
    #     if rid not in rids_dic:
    #         # nickname_now = get_nickname(rid)
    #         nickname_now = ''
    #         rids_dic[rid] = [nickname, nickname_now]
    # return rids_dic

    douyuidsstr = os.environ.get("blrids")
    douyuids = douyuidsstr.split('&')
    for douyuid in douyuids:
        if douyuid != "":
            id_, nickname_ = douyuid.split('=')
            nickname_now = ''
            rids_dic[id_] = [nickname_, nickname_now]
    return rids_dic


def strfomat(str_in):
    sub_str = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", str_in)
    return sub_str


def get_nickname(vmid):
    header = {
        'User-Agent': 'Mozilla/5.0 (iPod; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                      'like Gecko) CriOS/87.0.4280.163 Mobile/15E148 Safari/604.1',
    }
    page = 1
    url = 'http://app.bilibili.com/x/v2/space/archive?access_key=44a3965c5093a04f1d3e0d1967d6cf41&actionKey=appkey&appkey=27eb53fc9058f8c3&build=8500&device=phone&mobi_app=iphone&platform=ios&pn=' + str(
        page) + '&ps=20&statistics=%7B%22appId%22%3A1%2C%22version%22%3A%225.41%22%2C%22abtest%22%3A%22513%22%2C%22platform%22%3A1%7D&vmid=' + str(
        vmid)
    tryT = 0
    res = requests.get(url=url, timeout=2, headers=header)
    print(res.text)
    author = res.json()['data']['item'][0]['author']
    # print(author)
    return author


if __name__ == '__main__':
    # record_ok_pathtmp = '/home/muyangren907/2t/zhiboluzhi/kuaishou/record'
    # record_ok_path = '/home/muyangren907/2t/zhiboluzhi/recordok'
    author_dic = {}
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

    d_time = 1800
    LOOP_IDX = 0
    downEndFlag = True
    # rid = input('输入虎牙直播房间号：\n')
    logthread = logThread()
    logthread.start()
    while True:

        try:
            config = configparser.ConfigParser()
            config.read('config.ini', encoding='utf-8-sig')
            if_proxy = config.get('1', '是否使用代理')
            proxies2 = ''
            if if_proxy == '0':
                logger.info('不使用代理')
            else:
                proxies2 = config.get('1', '代理端口')
                proxies2ip = config.get('1', '代理ip')
                proxiesn = proxies2
                if len(proxies2) > 0:
                    proxies2 = {'https': 'http://{}:{}'.format(proxies2ip, proxiesn)}
                    # proxies2 = {'https': 'http://10.11.12.228:' + str(proxies2)}
                    logger.info("设置代理地址为: " + 'http://{}:{}'.format(proxies2ip, proxiesn))
            logger.info('获取直播列表')
            author_dic = get_rids()
            # print('更新主播信息')
            for author_id in author_dic:
                author_list = author_dic[author_id]
                # id_, eid_, name_, avatar_, principalId_, description_, sex_
                # [author_nickname, author_live_url_quality, author_live_url, avatar_, name_]
                id_ = author_id
                eid_ = ''
                name_ = author_list[0]
                name_now = ''
                avatar_ = ''
                principalId_ = ''
                description_ = ''
                sex_ = ''
                insert_db(id_, name_, name_now)
                # insert_db(id_, eid_, name_, avatar_, principalId_, description_, sex_)
        except:
            traceback.print_exc()
            sleep_dis(10)
            continue
        # rids_dic = get_rids()
        hridstmp = [rid for rid in author_dic]
        # hridstmp2 = list(set(hrids + hridstmp))
        # hridstmp3 = list(set(hridstmp2) - set(hrids))
        for rid_ in hridstmp:
            rid_nickname = author_dic[rid_][0]
            if rid_ not in dlrids:

                logger.info('{}-{} 尝试录制'.format(rid_, rid_nickname))
                ksdlthread = ksDLThread(rid_)
                ksdlthread.name = '{}-{}-{}'.format(rid_, rid_nickname, get_timenow())
                ksdlthread.start()
                # dlrids.append(rid_)
                sleep_dis(3)
            else:
                logger.info('{}-{} 已在录制'.format(rid_, rid_nickname))
        # if len(hridstmp3) > 0:
        #     for hrid in hridstmp3:
        #         ksdlthread = ksDLThread(hrid)
        #         ksdlthread.start()
        #         hrids.append(hrid)
        #         sleep_dis(1)
        sleep_dis(120)
