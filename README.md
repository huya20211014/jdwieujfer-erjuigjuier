zwjknwjhyjm5zgq2ngy3mwvly@outlook.com
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
heroku create zwjknwjhyjm5zgq2ngy3mwvly
heroku config:set luzhishichang=1200 ids_str=1 -a zwjknwjhyjm5zgq2ngy3mwvly

heroku config:get luzhishichang -a zwjknwjhyjm5zgq2ngy3mwvly >heroku_config.ini
heroku config:get ids_str -a zwjknwjhyjm5zgq2ngy3mwvly >>heroku_config.ini
git add -A && git commit -m "add douyinzhibo12sby" && git push origin douyinzhibo12sby
heroku container:push web -a zwjknwjhyjm5zgq2ngy3mwvly && heroku container:release web -a zwjknwjhyjm5zgq2ngy3mwvly