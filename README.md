zdg3ztaxmjhhnzbjm2i3ndm0y@outlook.com
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
heroku create zdg3ztaxmjhhnzbjm2i3ndm0y
heroku config:set luzhishichang=1200 ids_str=1 -a zdg3ztaxmjhhnzbjm2i3ndm0y

heroku config:get luzhishichang -a zdg3ztaxmjhhnzbjm2i3ndm0y >heroku_config.ini
heroku config:get ids_str -a zdg3ztaxmjhhnzbjm2i3ndm0y >>heroku_config.ini
git add -A && git commit -m "add douyinzhibo41sby" && git push origin douyinzhibo41sby
heroku container:push web -a zdg3ztaxmjhhnzbjm2i3ndm0y && heroku container:release web -a zdg3ztaxmjhhnzbjm2i3ndm0y