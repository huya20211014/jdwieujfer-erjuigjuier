ztdlmwjmyjjlywuwyjq2njawo@outlook.com
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
heroku create ztdlmwjmyjjlywuwyjq2njawo
heroku config:set luzhishichang=1200 ids_str=1 -a ztdlmwjmyjjlywuwyjq2njawo

heroku config:get luzhishichang -a ztdlmwjmyjjlywuwyjq2njawo >heroku_config.ini
heroku config:get ids_str -a ztdlmwjmyjjlywuwyjq2njawo >>heroku_config.ini
git add -A && git commit -m "add douyinzhibo05xby" && git push origin douyinzhibo05xby
heroku container:push web -a ztdlmwjmyjjlywuwyjq2njawo && heroku container:release web -a ztdlmwjmyjjlywuwyjq2njawo