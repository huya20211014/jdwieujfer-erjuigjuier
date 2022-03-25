# 使用说明

- 增加录制的python脚本 在herokusanic.py中指定录制脚本 重新生成sess 在up.py中指定录制前缀

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


- cc
```
odvmytliztfkzge@dslab2022.tk
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
heroku create odvmytliztfkzge

heroku config:set luzhishichang=1800 ids="400943235=婉柔&248792635=梓陌&351456178=安扬&354537294=漫妮&357418610=千代子子&368291563=莱傲_富婆抖抖&406420197=丸子超凶的&373228525=九儿&389962614=艺禾&384796337=大幂幂&407875781=妹妹&403420927=7879帝儿&272060=大锤妹妹&408240559=酒儿&406478715=温婉&351299617=狗蛋&359326974=静儿&358424549=小野马&369910883=嗲琪&403890993=白妖妖&369281763=莱傲_梓妍&358575804=朴西卡&365156479=可儿&386599406=晚晚&403268807=甜妹儿&394869073=莱傲_迪丽扎扎&" -a odvmytliztfkzge
git add -A && git commit -m "add ccxby01" && git push origin ccxby01
heroku container:push web -a odvmytliztfkzge && heroku container:release web -a odvmytliztfkzge
```