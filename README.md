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

- huyazhiboxby01
```
gigapic495@bubblybank.com

m2zkymflyjdhodm@dslab2022.tk
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
heroku create m2zkymflyjdhodm
git add -A && git commit -m "add huyazhiboxby01" && git push origin huyazhiboxby01
heroku container:push web -a m2zkymflyjdhodm && heroku container:release web -a m2zkymflyjdhodm

```
 

