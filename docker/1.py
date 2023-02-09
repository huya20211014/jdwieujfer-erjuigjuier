for i in range(1,23):
    key1 = 'dymcmn%02d'%i
    keyy = '{}xby'.format(key1)
    cmd = 'git checkout {} && git checkout douyinzhibo01xby -- douyinMulLiveAioHeroku.py'.format(keyy)
    
    cmd += "&& sed -i 's/douyinzhibo01_web/{}_web/g' douyinMulLiveAioHeroku.py".format(key1)
    cmd +='&& git add -A && git commit -m "add {}" && git push origin {}'.format(keyy,keyy)
    
    print(cmd)