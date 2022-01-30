# -*- coding: utf-8 -*-
# @Time    : 2021/9/16 11:12
# @Author  : muyangren907
# @Email   : myr907097904@gmail.com
# @File    : up.py
# @Software: PyCharm
import json
import os
import shutil
import threading
import time

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

def sleep_dis(sleep_time):
    for i in range(sleep_time, -1, -1):
        print('休眠 %5s s' % i, end='\r')
        time.sleep(1)


class upThread(threading.Thread):
    def __init__(self, upID, upthreadIDX):
        threading.Thread.__init__(self)
        self.upID = upID
        self.upthreadIDX = upthreadIDX
        self.configf = os.path.join(sess_path, '{}.json'.format(self.upID))
        self.UID = self.upID.split('_')[0]

        logger.info('Thread {} init'.format(self.upID))

    def gen_session(self):
        f = self.upID
        src_p = sess_path
        dst_p = sess_path
        jsonf = os.path.join(src_p, 'tg.json')
        sessf = os.path.join(src_p, 'tgup{}.session'.format(self.upthreadIDX % sess_total))
        jsonf1 = os.path.join(dst_p, '{}.json'.format(f))
        sessf1 = os.path.join(dst_p, '{}.session'.format(f))
        shutil.copy(jsonf, jsonf1)
        shutil.copy(sessf, sessf1)
        jfstr = ''
        with open(jsonf1, mode='r', encoding='utf-8') as jf:
            jfstr = jf.read()
        jfjson = json.loads(jfstr)
        jfjson['session'] = sessf1
        jfstr1 = json.dumps(jfjson)
        # logger.info(jfstr1)
        with open(jsonf1, mode='w', encoding='utf-8') as jf1:
            jf1.write(jfstr1)

    def del_session(self):
        f = self.upID
        src_p = sess_path
        dst_p = sess_path
        jsonf = os.path.join(src_p, 'tg.json')
        sessf = os.path.join(src_p, 'tg.session')
        jsonf1 = os.path.join(dst_p, '{}.json'.format(f))
        sessf1 = os.path.join(dst_p, '{}.session'.format(f))
        os.remove(jsonf1)
        os.remove(sessf1)

    # def movefile2OK(self, mp4fname):
    #     shutil.move(mp4fname, 'upok/')

    def run(self):
        logger.info('Thread {} started'.format(self.upID))
        try:
            if self.UID in config_dic:
                self.to_channel = config_dic[self.UID]

                if not os.path.exists(self.configf):
                    self.gen_session()
                upload_caption = self.upID.replace('[', ' ').replace(']', ' ').replace('(', ' ').replace(')', ' ')
                upload_caption = '{}_HerokuUP_{}'.format(upload_caption,UPLOAD_PRE)
                cmd = '{} -d --to {} --config "{}" --caption "{}" "recordok/{}"'.format(telegram_upload,
                                                                                     self.to_channel,
                                                                                     self.configf, upload_caption,
                                                                                     self.upID)
                logger.info('Thread {}: {}'.format(self.upID, cmd))
                os.system(cmd)
                logger.info('Thread {} upload finished!'.format(self.upID))
                # time.sleep(1)
                sleep_dis(1)
                logger.info('Thread {} clean'.format(self.upID))
                # self.movefile2OK(self.upID)
                self.del_session()
        except Exception as e:
            logger.info('{}'.format(e))
            try:
                self.del_session()
            except Exception as e:
                logger.info('{}'.format(e))
        global upthreads
        upthreads.remove(self.upID)
        logger.info('Thread {} exit'.format(self.upID))


def getmp4file(dir_in):
    mp4files = []
    for mp4_ in os.listdir(dir_in):
        for post_ in post_global:
            if post_ in mp4_:
                mp4files.append(mp4_)
                break
    # mp4files = [mp4_  if '.mp4' in mp4_ or '.jpg' in mp4_]
    mp4files.sort()
    return mp4files


def getconfig(config_path):
    # 51200,http://t.me/invite_link
    config_str = ''
    with open(config_path, mode='r', encoding='utf-8') as configf:
        config_str = configf.read()
    configlines = [con_ for con_ in config_str.split('\n') if con_ != '']
    config_dic = {}
    # qu chong
    for configline in configlines:
        uid, invitelink = configline.split(',')
        if uid not in config_dic:
            config_dic[uid] = invitelink
    # # write back
    # with open(config_path, mode='w', encoding='utf-8') as configf1:
    #     for uid in config_dic:
    #         configf1.write('{},{}\n'.format(uid, config_dic[uid]))
    return config_dic


def get_now_uids(mp4files):
    uids = list(set([uid.split('_')[0] for uid in mp4files]))
    uids.sort()
    return uids


if __name__ == '__main__':
    #ksmullive_idx = int(os.environ.get("ksmullive_idx"))
    UPLOAD_PRE = 'Douyin_dymcmm12'
    post_global = ['.mp4', '.jpg', '.jpeg', '.png', '.mov', '.MP4', '.JPG', '.JPEG', '.PNG', '.gif', '.GIF']
    max_thread_num_MAX = 15
    sess_path = 'sess'
    sess_total = 2
    config_path = 'up.ini'
    # proxy = 'socks5://127.0.0.1:1080'
    telegram_upload = 'telegram-upload'
    max_thread_num = max_thread_num_MAX

    # rmsesscmd = 'rm -rf {}/*mp4*'.format(sess_path)
    # logger.info(rmsesscmd)
    # os.system(rmsesscmd)

    if not os.path.exists(config_path):
        os.makedirs(config_path)

    loop_times = 0
    while True:
        loop_times += 1
        logger.info('循环次数 {}'.format(loop_times))
        logger.info('循环次数 {}'.format(loop_times))
        max_thread_num = max_thread_num_MAX
        mp4files = getmp4file('recordok')
        logger.info('本次上传视频数 {}'.format(len(mp4files)))
        logger.info('本次上传视频数 {}'.format(len(mp4files)))
        config_dic = getconfig(config_path)
        # time.sleep(5)
        sleep_dis(2)

        upthreads = []

        uids_idx = 0
        if max_thread_num > len(mp4files):
            max_thread_num = len(mp4files)
        for i in range(max_thread_num):
            # upt = upThread(mp4files[uids_idx])
            upthreads.append(mp4files[uids_idx])
            upthreadidx = upthreads.index(mp4files[uids_idx])
            upt = upThread(mp4files[uids_idx], upthreadidx)
            upt.start()
            uids_idx += 1
            # time.sleep(2)
            sleep_dis(1)

        while True:
            try:
                mp4filestmp = getmp4file('recordok')
                mp4filesdet = [m for m in mp4filestmp if m not in mp4files]
                # mp4filesdet = mp4filestmp
                mp4files += mp4filesdet

                max_thread_num = max_thread_num_MAX
                if max_thread_num > len(mp4files):
                    max_thread_num = len(mp4files)

                # logger.info('新增视频数目 {}'.format(len(mp4filesdet)))
                # logger.info('现共视频数目 {}'.format(len(mp4files)))
                # logger.info('max_thread_num {}'.format(max_thread_num))

                # logger.info('\nmp4 num {}'.format(len(mp4files)))
                config_dic = getconfig(config_path)
                # mp4files = [mp4file_ for mp4file_ in mp4files if mp4file_ not in upthreads]

                upthreadlen = len(upthreads)
                logger.info('uploading [{}/{} | {}] threads:'.format(threading.active_count() - 1, len(mp4files),
                                                                 len(mp4filestmp)))
                for i in range(upthreadlen):
                    logger.info("[ {} / {} ]{}".format(mp4files.index(upthreads[i]) + 1, len(mp4files), upthreads[i]))
                    
                if upthreadlen < max_thread_num_MAX and uids_idx < len(mp4files):
                    logger.info('upthreadlen < max_thread_num_MAX and uids_idx < len(mp4files)')
                    iiii = 0
                    while iiii < max_thread_num_MAX - upthreadlen and iiii < len(mp4files) - uids_idx:
                        upthreads.append(mp4files[uids_idx])
                        upthreadidx = upthreads.index(mp4files[uids_idx])
                        upt = upThread(mp4files[uids_idx], upthreadidx)
                        upt.start()
                        uids_idx += 1
                        iiii += 1
                elif uids_idx >= len(mp4files) and threading.active_count() == 1:
                    logger.info('uids_idx >= len(mp4files) and threading.active_count() == 1')
                    break
                time.sleep(2)
                # sleep_dis(2)
            except Exception as e:
                logger.info('{}'.format(e))
        time.sleep(1)