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
bzzb020211225@gmail.com

heroku login -i
heroku container:login
heroku create bilibilidocker1
heroku container:push web -a bilibilidocker1
heroku container:release web -a bilibilidocker1
```


- bzzb02
```
bilibilidocker2@outlook.com


yzvhmza0mzkwzdj@myr907.ml
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
heroku create yzvhmza0mzkwzdj

heroku config:set luzhishichang=1800 blrids="3328241=座山雕&22071218=耿清清&715=小须须&22820500=余多多&23414019=玥檬呀&22828499=慕儿&23858274=小艺&23739110=月神月柒&23273792=雪糕_Yuki7雪糕&1319379=徐珺_徐珺大哥&23587248=奶糖_憨憨小奶糖&21678026=兔牙_兔牙Sinar酱&23634221=格导师&912892=岚西啊喵&816238=御酱Asahi&24012358=Di宝宝&23448867=小桃气_你的小桃气呀&23237648=大长腿芙芙&23946408=甜诱小迷妹&919589=李礼礼可欣&938715=梦可御&23551267=喵可卿&3096485=周末yuuko&23981016=涵宝不睡懒觉&22940531=青禾_很嚣张的青禾&22698376=丝瑶姐姐&22689732=无敌大喵子&9863884=兔叽学妹&921260=ParmyAU&2926481=鱼朵瑜伽&" -a yzvhmza0mzkwzdj
git add -A && git commit -m "fix bugs" && git push origin bzzb02
heroku container:push web -a yzvhmza0mzkwzdj && heroku container:release web -a yzvhmza0mzkwzdj
```