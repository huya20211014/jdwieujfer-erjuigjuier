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

- kszbxby05
```
ksdocker1@outlook.com
Yttyhxways778!

zmnkogi5mzblyza@dslab2022.tk
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
heroku create zmnkogi5mzblyza
heroku config:set ksmullive_idx=5 -a zmnkogi5mzblyza
git add -A && git commit -m "add kszbxby05" && git push origin kszbxby05
heroku container:push web -a zmnkogi5mzblyza && heroku container:release web -a zmnkogi5mzblyza
```

