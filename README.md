# 使用说明

- 增加录制的python脚本 在herokusanic.py中指定录制脚本 重新生成sess 在up.py中指定录制前缀

1. 一号一sess
2. 参数设置 快手直播编号  快手直播总编号 cookies ksmullive_idx  ksmullive_tot
3. 按范围录制直播

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

heroku login -i
heroku container:login
heroku create douyudocker1
heroku container:push web -a douyudocker1
heroku container:release web -a douyudocker1
```


- cc1
```
ccdocker1@outlook.com

heroku login -i
heroku container:login
heroku create ccdocker1
heroku container:push web -a ccdocker1
heroku container:release web -a ccdocker1
```

- cc2
```
ccdocker2@outlook.com

heroku login -i
heroku container:login
heroku create ccdocker2
heroku container:push web -a ccdocker2
heroku container:release web -a ccdocker2
```

- afreecatv1
```
afreedocker1@outlook.com

heroku login -i
heroku container:login
heroku create afreedocker1
heroku container:push web -a afreedocker1
heroku container:release web -a afreedocker1
```

- afreecatv2
```
afreedocker2@outlook.com

heroku login -i
heroku container:login
heroku create afreedocker2
heroku container:push web -a afreedocker2 && heroku container:release web -a afreedocker2
```

- kszb01
```
ksdocker1@outlook.com
Yttyhxways778!

zdq3nja2ndczmdd@myr907.ml
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
heroku create zdq3nja2ndczmdd
heroku config:set ksmullive_idx=1 -a zdq3nja2ndczmdd
git add -A && git commit -m "add kszb01" && git push origin kszb01
heroku container:push web -a zdq3nja2ndczmdd && heroku container:release web -a zdq3nja2ndczmdd
```

kszb02


nzhimgfkmddjmza@dslab2022.tk
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
heroku create nzhimgfkmddjmza
heroku config:set ksmullive_idx=2 -a nzhimgfkmddjmza
git add -A && git commit -m "add kszb02" && git push origin kszb02
heroku container:push web -a nzhimgfkmddjmza && heroku container:release web -a nzhimgfkmddjmza
    

kszb02


nzhimgfkmddjmza@myr907.ml
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
heroku create nzhimgfkmddjmza
heroku config:set ksmullive_idx=2 -a nzhimgfkmddjmza
git add -A && git commit -m "add kszb02" && git push origin kszb02
heroku container:push web -a nzhimgfkmddjmza && heroku container:release web -a nzhimgfkmddjmza
    

kszb03


ntljntdiotc3odg@myr907.ml
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
heroku create ntljntdiotc3odg
heroku config:set ksmullive_idx=3 -a ntljntdiotc3odg
git add -A && git commit -m "add kszb03" && git push origin kszb03
heroku container:push web -a ntljntdiotc3odg && heroku container:release web -a ntljntdiotc3odg
    

kszb04


nmiyyjc2owvmyth@myr907.ml
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
heroku create nmiyyjc2owvmyth
heroku config:set ksmullive_idx=4 -a nmiyyjc2owvmyth
git add -A && git commit -m "add kszb04" && git push origin kszb04
heroku container:push web -a nmiyyjc2owvmyth && heroku container:release web -a nmiyyjc2owvmyth
    

kszb05


ntmymjg4zdu0ymq@myr907.ml
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
heroku create ntmymjg4zdu0ymq
heroku config:set ksmullive_idx=5 -a ntmymjg4zdu0ymq
git add -A && git commit -m "add kszb05" && git push origin kszb05
heroku container:push web -a ntmymjg4zdu0ymq && heroku container:release web -a ntmymjg4zdu0ymq
    

kszb06


owfkntliyjm5owj@myr907.ml
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
heroku create owfkntliyjm5owj
heroku config:set ksmullive_idx=6 -a owfkntliyjm5owj
git add -A && git commit -m "add kszb06" && git push origin kszb06
heroku container:push web -a owfkntliyjm5owj && heroku container:release web -a owfkntliyjm5owj
    

kszb07


yte1mjjhmzeymdg@myr907.ml
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
heroku create yte1mjjhmzeymdg
heroku config:set ksmullive_idx=7 -a yte1mjjhmzeymdg
git add -A && git commit -m "add kszb07" && git push origin kszb07
heroku container:push web -a yte1mjjhmzeymdg && heroku container:release web -a yte1mjjhmzeymdg
    

kszb08


ngqyogiwzjuwywn@myr907.ml
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
heroku create ngqyogiwzjuwywn
heroku config:set ksmullive_idx=8 -a ngqyogiwzjuwywn
git add -A && git commit -m "add kszb08" && git push origin kszb08
heroku container:push web -a ngqyogiwzjuwywn && heroku container:release web -a ngqyogiwzjuwywn
    

