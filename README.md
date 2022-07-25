mdg0odk3njlizdqxmdq1mmrjn@outlook.com
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
heroku create mdg0odk3njlizdqxmdq1mmrjn
heroku config:set luzhishichang=1200 ids_str=1 -a mdg0odk3njlizdqxmdq1mmrjn

heroku config:get luzhishichang -a mdg0odk3njlizdqxmdq1mmrjn >heroku_config.ini
heroku config:get ids_str -a mdg0odk3njlizdqxmdq1mmrjn >>heroku_config.ini
git add -A && git commit -m "add douyinzhibo04sby" && git push origin douyinzhibo04sby
heroku container:push web -a mdg0odk3njlizdqxmdq1mmrjn && heroku container:release web -a mdg0odk3njlizdqxmdq1mmrjn