mjy4oddhmtywmge2ymrlmdk4z@outlook.com
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
heroku create mjy4oddhmtywmge2ymrlmdk4z
heroku config:set luzhishichang=1200 ids_str=1 -a mjy4oddhmtywmge2ymrlmdk4z

heroku config:get luzhishichang -a mjy4oddhmtywmge2ymrlmdk4z >heroku_config.ini
heroku config:get ids_str -a mjy4oddhmtywmge2ymrlmdk4z >>heroku_config.ini
git add -A && git commit -m "add douyinzhibo27xby" && git push origin douyinzhibo27xby
heroku container:push web -a mjy4oddhmtywmge2ymrlmdk4z && heroku container:release web -a mjy4oddhmtywmge2ymrlmdk4z