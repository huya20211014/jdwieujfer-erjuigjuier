# -*- coding: utf-8 -*-
# @Time    : 2022/2/5 17:44
# @Author  : muyangren907
# @Email   : myr907097904@gmail.com
# @File    : herokuArgsSanic.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time    : 2021/10/10 20:47
# @Author  : muyangren907
# @Email   : myr907097904@gmail.com
# @File    : herokusanic.py
# @Software: PyCharm
import os
import threading
import time
import logging
import sanic
from sanic import Sanic
# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级开关
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)

class huyath(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                os.system('python3 ksMulLiveHeroku.py')
            except Exception as e:
                print(e)
                time.sleep(3)


class upth(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                os.system('python3 up.py')
            except Exception as e:
                print(e)
                time.sleep(3)


app = Sanic(name="HerokuSanic20211010")


def getsizestr(mp4_):
    bytessize = os.path.getsize(mp4_)
    dws = ['B', 'KB', 'MB', 'GB', 'TB']
    dwidx = 0
    while bytessize > 1024:
        bytessize /= 1024
        dwidx += 1
    return '{} {}'.format(bytessize, dws[dwidx])


@app.route('/')
async def index(request):
    huyadis = 'Hello World'
    return sanic.response.text(str(huyadis))


@app.route('/api', methods=['GET'])
async def api(request):
    logger.info('{}'.format(request.args))
    qury_type = request.args['query_type']
    qury_type_val = os.environ.get("{}".format(qury_type))
    # if qury_type_val is None:
    #     return sanic.response.text("抱歉 没有设置{}".format(qury_type))
    return sanic.response.text(qury_type_val)


# @app.route('/recordok')
# async def index(request):
#     huyadis = [mp4_ for mp4_ in os.listdir('recordok') if '.mp4' in mp4_]
#     huyalen = len(huyadis)
#     huyadis.sort()
#     responsestr = '<h>录制完成 {} 个</h></br>'.format(huyalen)
#     for mp4_ in huyadis:
#         responsestr+='<a>{} : {}</a></br>'.format(mp4_,getsizestr(os.path.join('recordok',mp4_)))
#     return sanic.response.html(responsestr)


# @app.route('/record')
# async def index(request):
#     huyadis = [mp4_ for mp4_ in os.listdir('record') if '.mp4' in mp4_]
#     huyalen = len(huyadis)
#     huyadis.sort()
#     responsestr = '<h>正在录制 {} 个</h></br>'.format(huyalen)
#     for mp4_ in huyadis:
#         responsestr+='<a>{} : {}</a></br>'.format(mp4_,getsizestr(os.path.join('record',mp4_)))
#     return sanic.response.html(responsestr)
#
# @app.route('/recordok')
# async def index(request):
#     huyadis = [mp4_ for mp4_ in os.listdir('recordok') if '.mp4' in mp4_]
#     huyalen = len(huyadis)
#     huyadis.sort()
#     responsestr = '<h>录制完成 {} 个</h></br>'.format(huyalen)
#     for mp4_ in huyadis:
#         responsestr+='<a>{} : {}</a></br>'.format(mp4_,getsizestr(os.path.join('recordok',mp4_)))
#     return sanic.response.html(responsestr)

if __name__ == '__main__':
    USE_PROXY = True
    # LISTEN_PORT = 8888
    # listen_port = LISTEN_PORT
    # huyathth = huyath()
    # huyathth.start()
    # upthth = upth()
    # upthth.start()

    app.run(host='0.0.0.0',
            port=int(os.environ.get('PORT', 8000)),
            workers=int(os.environ.get('WEB_CONCURRENCY', 1)),
            debug=bool(os.environ.get('DEBUG', '')))
