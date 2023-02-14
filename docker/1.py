for i in range(1,21):
    key1 = 'kszb%02d'%i
    keyy = '{}'.format(key1)
    cmd = 'git checkout {} && git checkout douyinzhibo01sby -- lovetree'.format(keyy)
    cmd += '&& git checkout {} && git checkout kszb01 -- ksMulLiveHeroku.py'.format(keyy)
    
    cmd += "&& sed -i 's/ksmullive_idx=1/ksmullive_idx={}/g' douyinMulLiveAioHeroku.py".format(i)
    cmd +='&& git add -A && git commit -m "add {}" && git push origin {}'.format(keyy,keyy)
    
    print(cmd)