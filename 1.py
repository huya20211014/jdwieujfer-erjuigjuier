mainbranch = 'dymcmn06'
mainbranch_hz = '{}xby'.format(mainbranch)
for i in range(1,23):
    key1 = 'dymcmn%02d'%i
    keyy = '{}xby'.format(key1)
    cmd = 'git checkout {} && git checkout {} -- douyinMulLiveAioHeroku.py'.format(keyy,mainbranch_hz)
    cmd += '&& git checkout {} && git checkout {} -- app.py'.format(keyy,mainbranch_hz)
    
    cmd += "&& sed -i 's/{}_web/{}_web/g' douyinMulLiveAioHeroku.py".format(mainbranch,key1)
    cmd += "&& sed -i 's/Douyin_{}/Douyin_{}/g' app.py".format(mainbranch_hz,keyy)
    cmd +='&& git add -A && git commit -m "add {}" && git push origin {}'.format(keyy,keyy)
    
    print(cmd)

for i in range(1,23):
    key1 = 'dymcmn%02d'%i
    keyy = '{}sby'.format(key1)
    cmd = 'git checkout {} && git checkout {} -- douyinMulLiveAioHeroku.py'.format(keyy,mainbranch_hz)
    cmd += '&& git checkout {} && git checkout {} -- app.py'.format(keyy,mainbranch_hz)
    
    cmd += "&& sed -i 's/{}_web/{}_web/g' douyinMulLiveAioHeroku.py".format(mainbranch,key1)
    cmd += "&& sed -i 's/Douyin_{}/Douyin_{}/g' app.py".format(mainbranch_hz,keyy)
    cmd +='&& git add -A && git commit -m "add {}" && git push origin {}'.format(keyy,keyy)
    
    print(cmd)
for i in range(1,49):
    key1 = 'douyinzhibo%02d'%i
    keyy = '{}sby'.format(key1)
    cmd = 'git checkout {} && git checkout {} -- douyinMulLiveAioHeroku.py'.format(keyy,mainbranch_hz)
    cmd += '&& git checkout {} && git checkout {} -- app.py'.format(keyy,mainbranch_hz)
    
    cmd += "&& sed -i 's/{}_web/{}_web/g' douyinMulLiveAioHeroku.py".format(mainbranch,key1)
    cmd += "&& sed -i 's/Douyin_{}/Douyin_{}/g' app.py".format(mainbranch_hz,keyy)
    cmd +='&& git add -A && git commit -m "add {}" && git push origin {}'.format(keyy,keyy)
    
    print(cmd)
for i in range(1,49):
    key1 = 'douyinzhibo%02d'%i
    keyy = '{}xby'.format(key1)
    cmd = 'git checkout {} && git checkout {} -- douyinMulLiveAioHeroku.py'.format(keyy,mainbranch_hz)
    cmd += '&& git checkout {} && git checkout {} -- app.py'.format(keyy,mainbranch_hz)
    
    cmd += "&& sed -i 's/{}_web/{}_web/g' douyinMulLiveAioHeroku.py".format(mainbranch,key1)
    cmd += "&& sed -i 's/Douyin_{}/Douyin_{}/g' app.py".format(mainbranch_hz,keyy)
    cmd +='&& git add -A && git commit -m "add {}" && git push origin {}'.format(keyy,keyy)
    
    print(cmd)