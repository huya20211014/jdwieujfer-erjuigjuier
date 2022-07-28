ymnkmjmxytbhndlhn2ywyjixn@outlook.com
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
heroku create ymnkmjmxytbhndlhn2ywyjixn
heroku config:set luzhishichang=1200 ids_str=1 -a ymnkmjmxytbhndlhn2ywyjixn

heroku config:get luzhishichang -a ymnkmjmxytbhndlhn2ywyjixn >heroku_config.ini
heroku config:get ids_str -a ymnkmjmxytbhndlhn2ywyjixn >>heroku_config.ini
git add -A && git commit -m "add douyinzhibo13sby" && git push origin douyinzhibo13sby
heroku container:push web -a ymnkmjmxytbhndlhn2ywyjixn && heroku container:release web -a ymnkmjmxytbhndlhn2ywyjixn