# 使用说明

- 增加录制的python脚本 在herokusanic.py中指定录制脚本 重新生成sess 在up.py中指定录制前缀

1. 一号一sess
2. 参数设置 快手直播编号  快手直播总编号 cookies ksmullive_idx  ksmullive_tot
3. 按范围录制直播

- 切记每次生成sess 并在config.ini中指定录制范围

- 生成命令

```
curl https://cli-assets.heroku.com/install.sh | sh
```
- huyadocer1
```
mianliuwang202107@gmail.com

heroku login -i
heroku container:login
heroku create huyadocker1
heroku container:push web -a huyadocker1
heroku container:release web -a huyadocker1
```

- huyadocer2
```
myr907097904@gmail.com

heroku login -i
heroku container:login
heroku create huyadocker2
heroku container:push web -a huyadocker2
heroku container:release web -a huyadocker2
```

- huyadocer3
```
chenbb2020@gmail.com

heroku login -i
heroku container:login
heroku create huyadocker3
heroku container:push web -a huyadocker3
heroku container:release web -a huyadocker3
```

- huyadocer4
```
muyangren9070979042021@gmail.com

heroku login -i
heroku container:login
heroku create huyadocker4
heroku container:push web -a huyadocker4
heroku container:release web -a huyadocker4
```

- bilibili1
```
bilibili20211225@gmail.com

heroku login -i
heroku container:login
heroku create bilibilidocker1
heroku container:push web -a bilibilidocker1
heroku container:release web -a bilibilidocker1
```

- douyu
```
jupyter20211226@outlook.com

heroku login -i
heroku container:login
heroku create douyudocker1
heroku container:push web -a douyudocker1
heroku container:release web -a douyudocker1
```


- cc1
```
ccdocker1@outlook.com

heroku login -i
heroku container:login
heroku create ccdocker1
heroku container:push web -a ccdocker1
heroku container:release web -a ccdocker1
```

- cc2
```
ccdocker2@outlook.com

heroku login -i
heroku container:login
heroku create ccdocker2
heroku container:push web -a ccdocker2
heroku container:release web -a ccdocker2
```

- afreecatv1
```
afreedocker1@outlook.com

heroku login -i
heroku container:login
heroku create afreedocker1
heroku container:push web -a afreedocker1
heroku container:release web -a afreedocker1
```

- afreecatv2
```
afreedocker2@outlook.com

heroku login -i
heroku container:login
heroku create afreedocker2
heroku container:push web -a afreedocker2 && heroku container:release web -a afreedocker2
```

- kuaishou1
```
ksdocker1@outlook.com

heroku login -i
heroku container:login
heroku create ksdocker1
heroku config:set ksmullive_idx=1 ksmullive_tot=10 cookies=ZGlkJiYmd2ViXzIwNzcxOTg0MTdhZWJmYmJjNDg5NDk0MzdiZmY3M2Y1JiYmJmRpZHYmJiYxNjMxMDE0MTI0MzY0JiYmJmNsaWVudGlkJiYmMyYmJiZjbGllbnRfa2V5JiYmNjU4OTBiMjkmJiYma3BuJiYmR0FNRV9aT05FJiYmJnVzZXJJZCYmJjY0NzQ0NjIxOCYmJiZrdWFpc2hvdS5saXZlLmJmYjFzJiYmM2UyNjExNDBiMGNmNzQ0NGEwYmE0MTFjNmYyMjdkODgmJiYma3VhaXNob3UubGl2ZS53ZWJfc3QmJiZDaFJyZFdGcGMyaHZkUzVzYVhabExuZGxZaTV6ZEJLZ0FVR0NPZ2RTUmJyQnZkSDlhZXhxdlVCTUd0dnlNV1J5QUtvbElxNFNmVTZESF9YcEw4d3J0MVZiOHhGMG0tQ3RYSl9KR3BpZ19WM2VGakxDd2VwQVA2QktEM2lZNkFpYmw5bElqYWYxYmVXZElfMGFnSXdHSUZjeTZqbGZyR0tkTDdwOTdGWmFJdnhRSzJ4RnZYSjhCRFNGUU5xZEhWMy1vWjl0eU40OFVNWTBXZnpkSko5Zi1LVUpabXNPTHNPX1F5MXB5VnhmUW91Mk1CXzdmTDNtS24wYUVnTDFjMWoxS0VlV3JPZTh4LXZUQzVuOWp5SWctNXZmZVRuRU9obDViNS1tQmhwUjJKOE5PcUNkTThkeVprTEpEOC1NM1Iwb0JUQUImJiYma3VhaXNob3UubGl2ZS53ZWJfcGgmJiZkZTQwNDk4YTRlY2Y1MDcwYWIxOTIxZTM4MWVkYjgxZGFkYzEmJiYm -a ksdocker1

heroku container:push web -a ksdocker1 && heroku container:release web -a ksdocker1
```

- douyin1
```
douyindocker1@outlook.com

heroku login -i
heroku container:login
heroku create douyindocker1
heroku config:set luzhishichang=1800 ids_str=aHR0cHM6Ly92LmRvdXlpbi5jb20vZXhlVEN3NS8s5Li75pKtOiDkuIrmtbfmsLjovr7lh6/ov6rmi4nlhYvmtabkuJzlupcKaHR0cHM6Ly92LmRvdXlpbi5jb20vZDJoZ2d2eS8s5Li75pKtOiDkuIrmtbfmsLjovr7lh6/ov6rmi4nlhYvmtabkuJzlupdf55Sc55Sc5Lya5Y+R5YWJCmh0dHBzOi8vdi5kb3V5aW4uY29tL1JGOTdYVkYvLOS4u+aSrTog5LiK5rW35rC46L6+5Yev6L+q5ouJ5YWL5rWm5Lic5bqXX+eUnOeUnOS8muWPkeWFiV/kuIDlj6rlgrvnmb3nlJzlkJYKaHR0cHM6Ly92LmRvdXlpbi5jb20vODVlZlVxNy8s5Li75pKtOiDljZbovabnvo7lpbNf5rC46L6+6LGq6L2m5rGHCmh0dHBzOi8vdi5kb3V5aW4uY29tLzhWdFNSZlQvLOS4u+aSrTog5Y2W6L2m576O5aWzX+awuOi+vuixqui9puS4reW/gwpodHRwczovL3YuZG91eWluLmNvbS9lOVVUUkFILyzkuLvmkq06IOWuieW+veawuOi+vuaNt+ixuei3r+iZjgpodHRwczovL3YuZG91eWluLmNvbS9leEhyV3JKLyzkuLvmkq06IEthcmlu5ou/6ZOB5Lu75YWs5a2QCmh0dHBzOi8vdi5kb3V5aW4uY29tL2V4Yk1IQjQvLOS4u+aSrTog5qyn6I+y5aWz546L5bCP5Y+3Cmh0dHBzOi8vdi5kb3V5aW4uY29tL2VnQnRmb28vLOS4u+aSrTog5qyn6I+y5aWz546L5bCP5Y+3Cmh0dHBzOi8vdi5kb3V5aW4uY29tL2VwZDhvaFAvLOS4u+aSrTog5qyn6I+y5aWz546LCmh0dHBzOi8vdi5kb3V5aW4uY29tL2RFaDJIbVgvLOS4u+aSrTog5qyn6I+y5aWz546LX+asp+iPsuWls+eOi+Wwj+WPtzEKaHR0cHM6Ly92LmRvdXlpbi5jb20vOHU1SFFkcC8s5Li75pKtOiDmrKfoj7LlpbPnjotf5qyn6I+y5aWz56WeCmh0dHBzOi8vdi5kb3V5aW4uY29tLzhHMkdzTXgvLOS4u+aSrTog5LiA6Lev6YKm5rG96L2m6Zmq57uDX+S4gOi3r+mCpgpodHRwczovL3YuZG91eWluLmNvbS9lZ0Jhc1IyLyzkuLvmkq06IOS4gOi3r+mCpuaxvei9pumZque7gwpodHRwczovL3YuZG91eWluLmNvbS84R2ozUm12LyzkuLvmkq06IOWNlui9pue+juWls1/lkIjogqXlroHljZrmsb3ovabplIDllK7mnInpmZDlhazlj7gKaHR0cHM6Ly92LmRvdXlpbi5jb20vZTRvclJ3bi8s5Li75pKtOiDlmInmrKMKaHR0cHM6Ly92LmRvdXlpbi5jb20vZTRvMmJMVC8s5Li75pKtOiBTZWxpbmEKaHR0cHM6Ly92LmRvdXlpbi5jb20vZTRvMm04cC8s5Li75pKtOiDpu4TlqIflqIcKaHR0cHM6Ly92LmRvdXlpbi5jb20vZTRvTTU5Mi8s5Li75pKtOiDokJ3mi4kKaHR0cHM6Ly92LmRvdXlpbi5jb20vZXhqN0Rwbi8s5Li75pKtOiDmgKfmhJ/okJ3mi4kKaHR0cHM6Ly92LmRvdXlpbi5jb20vODVlY2prdC8s5Li75pKtOiDmgKfmhJ/okJ3mi4lf5oCn5oSf566p5ouJCmh0dHBzOi8vdi5kb3V5aW4uY29tLzhHakFIQW4vLOS4u+aSrTog5Y2W6L2m576O5aWzX+aIkOmDveWkp+aYjOiFvui+vuS6jOaJi+i9puihjApodHRwczovL3YuZG91eWluLmNvbS9lRzQ2UjV4LyzkuLvmkq06IOWhnuWGt+S4nQpodHRwczovL3YuZG91eWluLmNvbS9kSGJhMWZDLyzkuLvmkq06IOWhnuWGt+S4nV/kuJ3lhrfloZ4KaHR0cHM6Ly92LmRvdXlpbi5jb20vZFc0ZmNyZy8s5Li75pKtOiDloZ7lhrfkuJ1f5Lid5Ya35aGe -a douyindocker1

heroku container:push web -a douyindocker1 && heroku container:release web -a douyindocker1
```

- dymcmm17
```
dymcmm17@dslab2021.me
Yttyhxways778!

heroku login -i
rm -rf sess/tgup*
python3 sessgen.py
mv tgup* sess
heroku container:login
heroku create dymcmm17
heroku config:set luzhishichang=1800 ids_str=aHR0cHM6Ly92LmRvdXlpbi5jb20vTFZCTGY4Ni8s5Li75pKtOiDljZbovabnvo7lpbNf5aKe5Z+O6Zu35YWL6JCo5pavCmh0dHBzOi8vdi5kb3V5aW4uY29tL0xWQmhnMXAvLOS4u+aSrTog5oqW6Z+z55u05pKtX+mbquWEvwpodHRwczovL3YuZG91eWluLmNvbS9MVmtFQkdtLyzkuLvmkq06IOWNlui9pue+juWls1/lpZTpqbDlk4jlsJTmu6jliKnmmJ8KaHR0cHM6Ly92LmRvdXlpbi5jb20vTFZCajhtVS8s5Li75pKtOiDmipbpn7Pnm7Tmkq1f6a2F5YS/Cmh0dHBzOi8vdi5kb3V5aW4uY29tL0xWQnV2R1IvLOS4u+aSrTog5oqW6Z+z55u05pKtX+iKiua+hApodHRwczovL3YuZG91eWluLmNvbS9MVkJnVUNSLyzkuLvmkq06IOaKlumfs+ebtOaSrV/lhZTlrZAK -a dymcmm17
git add -A && git commit -m "add dymcmm17" && git push origin dymcmm17
heroku container:push web -a dymcmm17 && heroku container:release web -a dymcmm17
```
