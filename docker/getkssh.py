# -*- coding: utf-8 -*-
# @Time    : 2022/3/26 20:34
# @Author  : muyangren907
# @Email   : myr907097904@gmail.com
# @File    : genkssh.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time    : 2022/2/21 14:52
# @Author  : muyangren907
# @Email   : myr907097904@gmail.com
# @File    : douyingensh.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time    : 2022/2/8 15:17
# @Author  : muyangren907
# @Email   : myr907097904@gmail.com
# @File    : genym.py
# @Software: PyCharm
import argparse
import base64
import hashlib
import os
parser = argparse.ArgumentParser()
parser.add_argument('--idx', type=str, default=None,
                    help='idx')
FLAGS = parser.parse_args()
IDX = FLAGS.idx
def base64encode(s):
    en = base64.b64encode(s.encode('utf-8'))
    return en.decode('utf-8')


def base64decode(a):
    de = base64.b64decode(a)
    return de.decode('utf-8')


def myren(strin):
    salt = '&&&hhj*（&&*……&*&%%…………&￥*&……**&……%&**#'
    salt = 'iijsjaksjkakjs&&&hhj*（&&*……&*&%%…………&￥*&……**&……%&**#'
    # 待加密信息
    str_ = '{}{}{}'.format(salt, strin, salt)
    # print(str_)
    # 创建md5对象
    hl = hashlib.md5()
    sh = hashlib.sha1()

    # Tips
    # 此处必须声明encode
    # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
    hl.update(str_.encode(encoding='utf-8'))

    sh.update(hl.hexdigest().encode('utf-8'))
    retsss = base64encode(sh.hexdigest())[:20]
    retsss = base64encode(hl.hexdigest())[:13]
    retsss = base64encode(hl.hexdigest())[:8]
    retsss = base64encode(sh.hexdigest())[:25]
    return retsss


def genym(i):
    ym = 'kszbxby%02d' % int(i)
    # ym = 'dymcmm%02d' % (i)
    ymret = myren(ym).lower()
    # print(ym, ymret)
    # print(ym, '{}@dslab2021.me'.format((ymret).lower()))
    # print(ym, 'https://{}.herokuapp.com/record'.format(ymret.lower()))
    return ym, ymret


def genids():
    ids_txt = 'douyin_heroku_ids.ini'
    ids_str = ''
    with open(ids_txt, mode='r', encoding='utf-8') as ids_f:
        ids_str = ids_f.read()
    return base64encode(ids_str)


def getids(ids_gen):
    # 特定id文件特定处理
    ids_dic = {}
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


def gen_id_bat_se(_type: int, spos: int, epos: int):
    ids_txt = 'douyinherokuid{}.ini'.format(_type)
    ids_str = ''
    with open(ids_txt, mode='r', encoding='utf-8') as ids_f:
        ids_str = ids_f.read()
    sline = spos - 1
    eline = epos
    ids_lines = [line_ for line_ in ids_str.split('\n')]
    ids_str = ''
    for i in range(sline, eline):
        if i >= len(ids_lines):
            break
        ids_str += '{}\n'.format(ids_lines[i])
    # print(ids_str)
    return base64encode(ids_str)


# _type 1 抖音直播    _type 2 卖车美女
def gen_id_bat(_type: int, _idx: int, tot=20):
    ids_txt = 'douyinherokuid{}.ini'.format(_type)
    ids_str = ''
    with open(ids_txt, mode='r', encoding='utf-8') as ids_f:
        ids_str = ids_f.read()
    sline = (_idx - 1) * tot
    eline = _idx * tot
    ids_lines = [line_ for line_ in ids_str.split('\n') if line_ != '']
    ids_str = ''
    for i in range(sline, eline):
        if i >= len(ids_lines):
            break
        ids_str += '{}\n'.format(ids_lines[i])
    # print(ids_str)
    return base64encode(ids_str)


def base64add(base641, base642):
    bde1 = base64decode(base641)
    bde2 = base64decode(base642)
    print(bde1)
    print(bde2)

    benret = base64encode('{}{}'.format(bde1, bde2))
    return benret


if __name__ == '__main__':
    idxxx = IDX
    # idxxx = 27
    email_ym = 'liuxinsb.cf'
    # email_ym = 'hotmail.com'
    for idxxx in range(1,2):
        ym, ymret = genym(idxxx)
        # if email_ym=='hotmail.com' and idxxx != 5:
        #     ymret='edwio{}'.format(ymret)
        # print('{}@dslab2021.me'.format((ymret).lower()))
        # print('{}@dslab2022.tk'.format((ymret).lower()))
        # print('Yttyhxways778!')
        # ids_str = gen_id_bat(1, idxxx, 100)
        # ids_str = gen_id_bat_se(2, 835, 888)
        prt_str = '''
    mkdir luzhi
    mkdir luzhichenggong
    touch luzhi/1.txt
    touch luzhichenggong/1.txt
    rm -rf sess/whynotlovexxxxxx*
    python3 sessgen.py
    mv whynotlovexxxxxx* sess
    heroku login -i
    heroku container:login
    heroku create {}
    heroku config:set ksmullive_idx={} -a {}
    git add -A && git commit -m "add kszbxby{}" && git push origin kszb
    heroku container:push web -a {} && heroku container:release web -a {}
        '''.format(ymret, idxxx,ymret, idxxx,ymret, ymret)
        print(prt_str)
        with open('../README.md',encoding='utf-8',mode='a+') as rdme:
            rdme.write('{}\n\n\n'.format(ym))

            rdme.write('{}@{}\n'.format((ymret).lower(),email_ym))
            rdme.write('Yttyhxways778!\n\n\n')
            rdme.write('{}\n'.format(prt_str))
            rdme.write('\n')
        os.system(prt_str)