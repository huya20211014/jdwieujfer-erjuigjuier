ngq5zgi0mzninme@dslab2021.me
Yttyhxways778!

rm -rf sess/tgup*
python3 sessgen.py
mv tgup* sess
heroku login -i
heroku container:login
heroku create ngq5zgi0mzninme
heroku config:set luzhishichang=1800 ids_str=aHR0cHM6Ly92LmRvdXlpbi5jb20vTEUyVjJydy8s5Li75pKtOiDljZbovabnvo7lpbNf5Y2h5LmD6amwCmh0dHBzOi8vdi5kb3V5aW4uY29tL0xFMnFjRFUvLOS4u+aSrTog5oqW6Z+z55u05pKtX+Wbm+W3neWPjOeriwpodHRwczovL3YuZG91eWluLmNvbS9MRTJjM3V2LyzkuLvmkq06IOaKlumfs+ebtOaSrV/mnLXllaYKaHR0cHM6Ly92LmRvdXlpbi5jb20vTEUyUU53MS8s5Li75pKtOiDmipbpn7Pnm7Tmkq1f55Sc5bmC5bmCCmh0dHBzOi8vdi5kb3V5aW4uY29tL0xFamhBYTIvLOS4u+aSrTog5oqW6Z+z55u05pKtX+WPr+S5kApodHRwczovL3YuZG91eWluLmNvbS9MRWoyTHdtLyzkuLvmkq06IOaKlumfs+ebtOaSrV/mtoLmtoIKaHR0cHM6Ly92LmRvdXlpbi5jb20vTEUyRXRiSC8s5Li75pKtOiDljZbovabnvo7lpbNf5rOJ5bee5LqM5omL6L2mCmh0dHBzOi8vdi5kb3V5aW4uY29tL0xFakw4TWEvLOS4u+aSrTog5Y2W6L2m576O5aWzX+mdkuWym+axvei9pgpodHRwczovL3YuZG91eWluLmNvbS9MRWpyVW1rLyzkuLvmkq06IOaKlumfs+ebtOaSrV/mgqDmgqAKaHR0cHM6Ly92LmRvdXlpbi5jb20vTEVqZDlvNC8s5Li75pKtOiDljZbovabnvo7lpbNf5ZSQ5bGx5LyX5LiA5rG96L2mCg== -a ngq5zgi0mzninme

heroku config:get luzhishichang -a ngq5zgi0mzninme >heroku_config.ini
heroku config:get ids_str -a ngq5zgi0mzninme >>heroku_config.ini
git add -A && git commit -m "add dyzb26" && git push origin dyzb26
heroku container:push web -a ngq5zgi0mzninme && heroku container:release web -a ngq5zgi0mzninme