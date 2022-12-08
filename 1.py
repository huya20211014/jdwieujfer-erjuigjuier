for i in range(1,21):
    keyy = 'kszb{:0>2d}'.format(i)
    # print(keyy)
    cmd = 'git checkout {} &&  git checkout kszb -- docker && git add -A && git commit -m "add {}" && git push origin {}'.format(keyy,keyy,keyy)
    print(cmd)