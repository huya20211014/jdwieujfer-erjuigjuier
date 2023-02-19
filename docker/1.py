for i in range(1,49):
    key1 = 'douyinzhibo%02d'%i
    keyy = '{}xby'.format(key1)
    cmd = 'git checkout {} && git checkout douyinzhibo08xby -- douyinMulLiveAioHeroku.py'.format(keyy)
    
    cmd += "&& sed -i 's/douyinzhibo08_web/{}_web/g' douyinMulLiveAioHeroku.py".format(key1)
    cmd +='&& git add -A && git commit -m "add {}" && git push origin {}'.format(keyy,keyy)
    
    print(cmd)