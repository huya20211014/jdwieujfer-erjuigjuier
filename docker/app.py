# -*- coding: utf-8 -*-
# @Time    : 2021/9/16 11:12
# @Author  : muyangren907
# @Email   : myr907097904@gmail.com
# @File    : app.py
# @Software: PyCharm
import json
import os
import shutil
import threading
import time
import requests
import logging  # 引入logging模块
import base64
def base64decode(a):
    de = base64.b64decode(a)
    return de.decode('utf-8')

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


class xxxxThread(threading.Thread):
    def __init__(self, xxxxID, xxxxthreadIDX):
        threading.Thread.__init__(self)
        self.xxxxID = xxxxID
        self.xxxxthreadIDX = xxxxthreadIDX
        self.configf = os.path.join(sess_path, '{}.json'.format(self.xxxxID))
        self.UID = self.xxxxID.split('_')[0]

        logger.info('Thread {} init'.format(self.xxxxID))

    def gen_session(self):
        f = self.xxxxID
        src_p = sess_path
        dst_p = sess_path
        jsonf = os.path.join(src_p, 'whynotlove.json')
        sessf = os.path.join(src_p, 'whynotlovexxxxxx{}.session'.format(self.xxxxthreadIDX % sess_total))
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
        f = self.xxxxID
        src_p = sess_path
        dst_p = sess_path
        jsonf = os.path.join(src_p, 'whynotlove.json')
        sessf = os.path.join(src_p, 'whynotlove.session')
        jsonf1 = os.path.join(dst_p, '{}.json'.format(f))
        sessf1 = os.path.join(dst_p, '{}.session'.format(f))
        os.remove(jsonf1)
        os.remove(sessf1)

    # def movefile2OK(self, mp4fname):
    #     shutil.move(mp4fname, 'xxxxok/')

    def run(self):
        logger.info('Thread {} started'.format(self.xxxxID))
        try:
            if self.UID in config_dic:
                self.to_channel = config_dic[self.UID]

                if not os.path.exists(self.configf):
                    self.gen_session()
                
                xxxxload_caption = self.xxxxID.replace('[', ' ').replace(']', ' ').replace('(', ' ').replace(')', ' ')
                xxxxload_caption = '{}_Herokuxxxx_{}'.format(xxxxload_caption,xxxxLOAD_PRE)
                cmd = '{} -d --to {} --config "{}" --caption "{}" "luzhichenggong/{}"'.format(telegram_xxxxload,
                                                                                     self.to_channel,
                                                                                     self.configf, xxxxload_caption,
                                                                                     self.xxxxID)
                logger.info('Thread {}: {}'.format(self.xxxxID, cmd))
                os.system(cmd)
                logger.info('Thread {} xxxxload finished!'.format(self.xxxxID))
                # time.sleep(1)
                sleep_dis(1)
                logger.info('Thread {} clean'.format(self.xxxxID))
                # self.movefile2OK(self.xxxxID)
                self.del_session()
        except Exception as e:
            logger.info('{}'.format(e))
            try:
                self.del_session()
            except Exception as e:
                logger.info('{}'.format(e))
        global xxxxthreads
        xxxxthreads.remove(self.xxxxID)
        logger.info('Thread {} exit'.format(self.xxxxID))


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


import traceback
def getherokuargs(query_type):
    # h_url = 'https://owziotrlotjimdv.herokuapp.com/api?query_type={}'.format(query_type)
    h_url = 'https://raw.githubusercontent.com/xiaosijitest/weioferiogeroijiii/main/{}'.format(query_type)

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

def getconfig(config_path):
    # 51200,http://t.me/invite_link
    config_str = ''
    with open(config_path, mode='r', encoding='utf-8') as configf:
        config_str = configf.read()
    # config_str = getherokuargs('app.exe')
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


def get_uflag():
    uflag = False
    res = requests.get('https://raw.githubusercontent.com/xiaosijitest/weioferiogeroijiii/main/dyini.ini')
    restext = res.text
    if restext=='no':
        uflag = False
    elif restext=='yes':
        uflag = True
    return uflag

if __name__ == '__main__':
    #ksmullive_idx = int(os.environ.get("ksmullive_idx"))
    xxxxLOAD_PRE = 'Douyin_dymcmn04xby'
    post_global = ['.tt','.mp4', '.jpg', '.jpeg', '.png', '.mov', '.MP4', '.JPG', '.JPEG', '.PNG', '.gif', '.GIF']
    # post_global = []
    max_thread_num_MAX = 2
    sess_path = 'huihua'
    sess_total = 2
    config_path = 'app.exe'
    # proxy = 'socks5://127.0.0.1:1080'
    telegram_xxxxload = 'neofetch'
    max_thread_num = max_thread_num_MAX

    # rmsesscmd = 'rm -rf {}/*mp4*'.format(sess_path)
    # logger.info(rmsesscmd)
    # os.system(rmsesscmd)

    if not os.path.exists(config_path):
        os.makedirs(config_path)

    loop_times = 0
    
    while True:
        # uflag = get_uflag()
        # if not uflag:
        #     logger.info('uflag {}'.format(uflag))
        #     sleep_dis(120)
        #     continue
        loop_times += 1
        logger.info('xhcs {}'.format(loop_times))
        logger.info('xhcs {}'.format(loop_times))
        max_thread_num = max_thread_num_MAX
        mp4files = getmp4file('luzhichenggong')
        logger.info('xxxx num {}'.format(len(mp4files)))
        logger.info('xxxx num {}'.format(len(mp4files)))
        config_dic = getconfig(config_path)
        # time.sleep(5)
        sleep_dis(2)

        xxxxthreads = []

        uids_idx = 0
        if max_thread_num > len(mp4files):
            max_thread_num = len(mp4files)
        
        for i in range(max_thread_num):
            # xxxxt = xxxxThread(mp4files[uids_idx])
            xxxxthreads.append(mp4files[uids_idx])
            xxxxthreadidx = xxxxthreads.index(mp4files[uids_idx])
            xxxxt = xxxxThread(mp4files[uids_idx], xxxxthreadidx)
            xxxxt.start()
            uids_idx += 1
            # time.sleep(2)
            sleep_dis(1)

        while True:
            try:
                mp4filestmp = getmp4file('luzhichenggong')
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
                # mp4files = [mp4file_ for mp4file_ in mp4files if mp4file_ not in xxxxthreads]

                xxxthlll = len(xxxxthreads)
                logger.info('xxx [{}/{} | {}]:'.format(threading.active_count() - 1, len(mp4files),
                                                                 len(mp4filestmp)))
                for i in range(xxxthlll):
                    logger.info("[ {} / {} ]{}".format(mp4files.index(xxxxthreads[i]) + 1, len(mp4files), xxxxthreads[i]))
                    
                if xxxthlll < max_thread_num_MAX and uids_idx < len(mp4files):
                    logger.info('xxxthlll < max_thread_num_MAX and uids_idx < len(mp4files)')
                    iiii = 0
                    while iiii < max_thread_num_MAX - xxxthlll and iiii < len(mp4files) - uids_idx:
                        xxxxthreads.append(mp4files[uids_idx])
                        xxxxthreadidx = xxxxthreads.index(mp4files[uids_idx])
                        xxxxt = xxxxThread(mp4files[uids_idx], xxxxthreadidx)
                        xxxxt.start()
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