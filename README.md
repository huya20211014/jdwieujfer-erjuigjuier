yjiznzg1mtjkyji1nmmyztvhn@outlook.com
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
heroku create yjiznzg1mtjkyji1nmmyztvhn
heroku config:set luzhishichang=1200 ids_str=1 -a yjiznzg1mtjkyji1nmmyztvhn

heroku config:get luzhishichang -a yjiznzg1mtjkyji1nmmyztvhn >heroku_config.ini
heroku config:get ids_str -a yjiznzg1mtjkyji1nmmyztvhn >>heroku_config.ini
git add -A && git commit -m "add douyinzhibo06xby" && git push origin douyinzhibo06xby
heroku container:push web -a yjiznzg1mtjkyji1nmmyztvhn && heroku container:release web -a yjiznzg1mtjkyji1nmmyztvhn