mtgznjmxn2ixndfiyze5y2vjm@outlook.com
Yttyhxways778!

mkdir luzhi
mkdir luzhichenggong
touch luzhi/1.txt
touch luzhichenggong/1.txt
rm -rf sess/whynotlovexxxxxx*
python3 sessgen.py
mv whynotlovexxxxxx* sess
heroku login -i
heroku container:login
heroku create mtgznjmxn2ixndfiyze5y2vjm
heroku config:set luzhishichang=1200 ids_str=1 -a mtgznjmxn2ixndfiyze5y2vjm

heroku config:get luzhishichang -a mtgznjmxn2ixndfiyze5y2vjm >heroku_config.ini
heroku config:get ids_str -a mtgznjmxn2ixndfiyze5y2vjm >>heroku_config.ini
git add -A && git commit -m "add douyinzhibo29sby" && git push origin douyinzhibo29sby
heroku container:push web -a mtgznjmxn2ixndfiyze5y2vjm && heroku container:release web -a mtgznjmxn2ixndfiyze5y2vjm