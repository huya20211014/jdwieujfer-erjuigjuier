ndkxmjqzywe1zjq0yzjhmjcwy@outlook.com
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
heroku create ndkxmjqzywe1zjq0yzjhmjcwy
heroku config:set luzhishichang=1200 ids_str=1 -a ndkxmjqzywe1zjq0yzjhmjcwy

heroku config:get luzhishichang -a ndkxmjqzywe1zjq0yzjhmjcwy >heroku_config.ini
heroku config:get ids_str -a ndkxmjqzywe1zjq0yzjhmjcwy >>heroku_config.ini
git add -A && git commit -m "add douyinzhibo18sby" && git push origin douyinzhibo18sby
heroku container:push web -a ndkxmjqzywe1zjq0yzjhmjcwy && heroku container:release web -a ndkxmjqzywe1zjq0yzjhmjcwy