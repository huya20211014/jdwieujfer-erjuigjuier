# 使用说明

- 切记每次生成sess 并在config.ini中指定录制范围

- 生成命令

```
curl https://cli-assets.heroku.com/install.sh | sh
```
- huyadocer1
```
mianliuwang202107@gmail.com

heroku login -i
heroku container:login
heroku create huyadocker1
heroku container:push web -a huyadocker1
heroku container:release web -a huyadocker1
```

- huyadocer2
```
myr907097904@gmail.com

heroku login -i
heroku container:login
heroku create huyadocker2
heroku container:push web -a huyadocker2
heroku container:release web -a huyadocker2
```

- huyadocer3
```
chenbb2020@gmail.com

heroku login -i
heroku container:login
heroku create huyadocker3
heroku container:push web -a huyadocker3
heroku container:release web -a huyadocker3
```

- huyadocer4
```
muyangren9070979042021@gmail.com

heroku login -i
heroku container:login
heroku create huyadocker4
heroku container:push web -a huyadocker4
heroku container:release web -a huyadocker4
```

- bilibili1
```
bilibili20211225@gmail.com

heroku login -i
heroku container:login
heroku create bilibilidocker1
heroku container:push web -a bilibilidocker1
heroku container:release web -a bilibilidocker1
```

- douyu
```
jupyter20211226@outlook.com

m2nknmix@googlr.cf
Yttyhxways778!

mkdir record
mkdir recordok
touch record/1.txt
touch recordok/1.txt
rm -rf sess/tgup*
python3 sessgen.py
mv tgup* sess
heroku login -i
heroku container:login
heroku create m2nknmix
heroku config:set luzhishichang=1800 douyuids="10337137=杨超越&7746333=奶优米&109064=尧顺宇&4624967=腐团儿&462228=隔壁的苏苏s&6677800=傲娇的喵小八&22619=Minana&6863470=唐星儿&6515025=何菱&6208237=球球Emma&6505338=上蓝冰儿&7753315=七姑娘小梧桐&9945289=爱跳舞的肉肉&6939197=李小婉&8998792=奈奈&71690=陈叨叨&9516609=狐苏&10109975=李嫣然&9545293=甜小桃&5440020=小小玉酱&10432719=抠门三儿&291260=酥念儿&6381492=曦曦Stacey&9243236=阿喜&123111=拉拉&10484268=用飘柔的小姐姐&700=张琪格&968987=南妹儿&7524314=猫痒痒lisa酱&" -a m2nknmix
git add -A && git commit -m "add douyu01" && git push origin douyu01
heroku container:push web -a m2nknmix && heroku container:release web -a m2nknmix
```

