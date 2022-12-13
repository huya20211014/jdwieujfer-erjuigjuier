for i in range(3,49):
    keyy = 'douyinzhibo%02dsby'%i
    cmd = 'git checkout {} &&  git checkout douyinzhibo01sby -- Dockerfile && git add -A && git commit -m "add {}" && git push origin {}'.format(keyy,keyy,keyy)
    print(cmd)