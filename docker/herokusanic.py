# -*- coding: utf-8 -*-
# @Time    : 2021/10/10 20:47
# @Author  : muyangren907
# @Email   : myr907097904@gmail.com
# @File    : herokusanic.py
# @Software: PyCharm
import sanic
import threading
import configparser
import logging
import traceback
import os
from sanic import Sanic
import time
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

class huyath(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                logger.info('python3 douyinMulLiveAioHeroku.py')
                os.system('python3 douyinMulLiveAioHeroku.py')
            except Exception as e:
                print(e)
                logger.info('{}'.format(e))
                traceback.print_exc()
                time.sleep(3)


class upth(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                os.system('python3 up.py')
            except Exception as e:
                traceback.print_exc()
                print(e)
                time.sleep(3)


app = Sanic(name="HerokuSanic20211010")

def getsizestr(mp4_):
    bytessize = os.path.getsize(mp4_)
    dws = ['B','KB','MB','GB','TB']
    dwidx = 0
    while bytessize>1024:
        bytessize/=1024
        dwidx +=1
    return '{} {}'.format(bytessize,dws[dwidx])

@app.route('/')
async def index(request):
    huyadis = 'are you come?'
    return sanic.response.text(str(huyadis))


@app.route('/record')
async def index(request):
    huyadis = [mp4_ for mp4_ in os.listdir('record') if '.mp4' in mp4_]
    huyalen = len(huyadis)
    huyadis.sort()
    responsestr = '<h>正在录制 {} 个</h></br>'.format(huyalen)
    for mp4_ in huyadis:
        responsestr+='<a>{} : {}</a></br>'.format(mp4_,getsizestr(os.path.join('record',mp4_)))
    return sanic.response.html(responsestr)

@app.route('/recordok')
async def index(request):
    huyadis = [mp4_ for mp4_ in os.listdir('recordok') if '.mp4' in mp4_]
    huyalen = len(huyadis)
    huyadis.sort()
    responsestr = '<h>录制完成 {} 个</h></br>'.format(huyalen)
    for mp4_ in huyadis:
        responsestr+='<a>{} : {}</a></br>'.format(mp4_,getsizestr(os.path.join('recordok',mp4_)))
    return sanic.response.html(responsestr)

if __name__ == '__main__':
    _dir_chk = 'record'
    if not os.path.exists(_dir_chk):
        os.makedirs(_dir_chk)
    _dir_chk = 'recordok'
    if not os.path.exists(_dir_chk):
        os.makedirs(_dir_chk)

    USE_PROXY = True
    # LISTEN_PORT = 8888
    # listen_port = LISTEN_PORT
    huyathth = huyath()
    huyathth.start()
    upthth = upth()
    upthth.start()

    app.run(host='0.0.0.0',
            port=int(os.environ.get('PORT', 8000)),
            workers=int(os.environ.get('WEB_CONCURRENCY', 1)),
            debug=bool(os.environ.get('DEBUG', '')))