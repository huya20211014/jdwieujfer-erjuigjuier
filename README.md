zjnkyjkynjc3otqwogziodqym@outlook.com
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
heroku create zjnkyjkynjc3otqwogziodqym
heroku config:set luzhishichang=1200 ids_str=1 -a zjnkyjkynjc3otqwogziodqym

heroku config:get luzhishichang -a zjnkyjkynjc3otqwogziodqym >heroku_config.ini
heroku config:get ids_str -a zjnkyjkynjc3otqwogziodqym >>heroku_config.ini
git add -A && git commit -m "add douyinzhibo47sby" && git push origin douyinzhibo47sby
heroku container:push web -a zjnkyjkynjc3otqwogziodqym && heroku container:release web -a zjnkyjkynjc3otqwogziodqym