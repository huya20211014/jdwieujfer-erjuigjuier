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
import os
from sanic import Sanic
import time


class huyath(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                os.system('python3 huyaMulLive.py')
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


@app.route('/')
async def index(request):
    huyadis = 'Hello World'
    return sanic.response.text(str(huyadis))


@app.route('/huya')
async def index(request):
    huyadis = [mp4_ for mp4_ in os.listdir('.') if '.mp4' in mp4_]
    huyalen = len(huyadis)
    huyadis.sort()
    responsestr = '<h>正在录制 {} 个</h></br>'.format(huyalen)
    for mp4_ in huyadis:
        responsestr+='<a>{}</a></br>'.format(mp4_)
    return sanic.response.html(responsestr)

@app.route('/recordok')
async def index(request):
    huyadis = [mp4_ for mp4_ in os.listdir('recordok') if '.mp4' in mp4_]
    huyalen = len(huyadis)
    huyadis.sort()
    responsestr = '<h>正在上传 {} 个</h></br>'.format(huyalen)
    for mp4_ in huyadis:
        responsestr+='<a>{}</a></br>'.format(mp4_)
    return sanic.response.html(responsestr)

if __name__ == '__main__':
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
