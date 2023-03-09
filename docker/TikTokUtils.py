#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@Description:TikTok.py
@Date       :2023/01/27 19:36:18
@Author     :muyangren907
@version    :1.0
@Github     :https://github.com/muyangren907
@Mail       :admin@muyangren907.com
-------------------------------------------------
Change Log  :
-------------------------------------------------
'''
import os
import random
import re
import json
import requests
from TikTokUrls import Urls
import datetime
import time
import logging
from rich.logging import RichHandler

import execjs
import urllib.parse


class Utils(object):
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            datefmt="[%x %X]",
            handlers=[RichHandler(rich_tracebacks=True)]
        )
        self.log = logging.getLogger("rich")

        pass

    def sleep_dis(self, sleep_time):
        for i in range(sleep_time, -1, -1):
            print('休眠 %5s s' % i, end='\r')
            time.sleep(1)

    def getlogger(self):
        return self.log

    def strfomat(self, str_in):
        sub_str = re.sub(
            u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", str_in)
        return sub_str

    def timestamp2strtime(self, timestamp):
        """将 13 位整数的毫秒时间戳转化成本地普通时间 (字符串格式)
        :param timestamp: 13 位整数的毫秒时间戳 (1456402864242)
        :return: 返回字符串格式 {str}'2016-02-25 20:21:04.242000'
        """
        local_str_time = datetime.datetime.fromtimestamp(timestamp / 1000.0).strftime('%Y_%m_%d_%H_%M_%S')
        return local_str_time

    def strtime2strtime(self, timestr):
        timeArray = time.strptime(timestr, "%Y-%m-%d %H.%M.%S")
        otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", timeArray)
        return otherStyleTime

    def getAllUserFile(self, root_dir):
        # print('正在获取已存在的作者信息')
        self.log.info('正在获取已存在的作者信息')
        au_dirs = os.listdir(root_dir)
        zzxxs = {}

        for au_dir in au_dirs:
            sec_uid = ''
            # print('正在获取')
            au_dir_abs = os.path.join(root_dir, au_dir)
            # print('正在获取 {}'.format(au_dir_abs))
            self.log.info('正在获取 {}'.format(au_dir_abs))
            if not os.path.isdir(au_dir_abs):
                continue
            zzxx = os.path.join(au_dir_abs, '作者信息.txt')
            zzxxstr = ''
            with open(zzxx, mode='r', encoding='utf-8') as zzxxf:
                zzxxstr = zzxxf.read()
            for iii in zzxxstr.split('\n'):
                if '作者SEC_UID：' in iii:
                    sec_uid = iii.replace('作者SEC_UID：', '')
                    # zzxxdic={}
                    # zzxxdic['sec_uid']=au_dir_abs
                    zzxxs[sec_uid] = au_dir_abs
                    break
        return zzxxs

    def generate_random_str(self, randomlength=16):
        """
        根据传入长度产生随机字符串
        """
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789='
        length = len(base_str) - 1
        for _ in range(randomlength):
            random_str += base_str[random.randint(0, length)]
        return random_str

    def replaceStr(self, filenamestr: str):
        """
        替换非法字符，缩短字符长度，使其能成为文件名
        """
        # 匹配 汉字 字母 数字 空格
        match = "([0-9A-Za-z\u4e00-\u9fa5 -._]+)"

        result = re.findall(match, filenamestr)

        result = "".join(result).strip()
        if len(result) > 80:
            result = result[:80]
        # 去除前后空格
        return result

    def getXbogus(self, url, headers=None):
        urls = Urls()
        base_url = '{}{}'.format(urls.GET_XB_PATH, url)
        self.log.debug('获取 {} 的 Xbogus'.format(base_url))
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        query = urllib.parse.urlparse(base_url).query
        xbogus = execjs.compile(open('./X-Bogus.js').read()).call('sign', query, user_agent)
        self.log.debug('获取到 Xbogus = {}'.format(xbogus))
        params = '{}&X-Bogus={}'.format(query, xbogus)
        # url =

        # try:
        #     response = json.loads(requests.post(
        #         url=urls.GET_XB_PATH, data={"param": url}, headers=headers, timeout=10).text)
        #     params = response["param"]
        #     xb = response["X-Bogus"]
        # except Exception as e:
        #     self.log.exception('[  错误  ]:X-Bogus接口异常, 可能是访问流量高, 接口限流请稍等几分钟再次尝试')
        #     # print('[  错误  ]:X-Bogus接口异常, 可能是访问流量高, 接口限流请稍等几分钟再次尝试')
        #     return -1
        # params = xbogus
        return params  # , xb

    def str2bool(self, v):
        if isinstance(v, bool):
            return v
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            return True


if __name__ == "__main__":
    pass
