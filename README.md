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
heroku config:set ksmullive_idx=1 ksmullive_tot=10 cookies=ZGlkJiYmd2ViXzIwNzcxOTg0MTdhZWJmYmJjNDg5NDk0MzdiZmY3M2Y1JiYmJmNsaWVudGlkJiYmMyYmJiZjbGllbnRfa2V5JiYmNjU4OTBiMjkmJiYma3BuJiYmR0FNRV9aT05FJiYmJnVzZXJJZCYmJjY0NzQ0NjIxOCYmJiZrdWFpc2hvdS5saXZlLmJmYjFzJiYmYWM1ZjI3YjNiNjI4OTU4NTljNGMxNjIyZjQ5ODU2YTQmJiYmZGlkdiYmJjE2NDE5MTYxNTcwMDAmJiYma3VhaXNob3UubGl2ZS53ZWJfc3QmJiZDaFJyZFdGcGMyaHZkUzVzYVhabExuZGxZaTV6ZEJLZ0FlT1B6bjBJUERST0g5TEtqV01qbzhORDYzT2Z0M3E2TXBUZjRncmIyS0Q2YVhjRnJiVjJPLTZIMFRyWDZzLVl2cTBTNnBLcFk2VzRUcUl4VC12NWdPNWp1a0hfa2ItSXBvc1lUX3J0a2I5bWlQcmVvdDVKcWE1LTRpdFhCby1qTllZVVpTN1FGcGtsTEp6bzJFcFFJeV80RVJXQVNQbzBGbHczaVlYckZGa1Rob1loYWZJVVJCYWhOLWpXNTVJMjZ6UzdrSHV6c3c4UXh0S3Q5dFYyaXhvYUVnVnMxTlVHTmtobGk5ZVVBdmNKdENxTXNpSWdkNERSWFJ5UnJac1pSSEpLNnR3b2FVVjBJRDE2dWZJN1FzdFEybTlEYmZzb0JUQUImJiYma3VhaXNob3UubGl2ZS53ZWJfcGgmJiZhYTRjNjQ4YjMwNmVkODg3OTIwYjAzZmIxMmM0ODRkYmI4MDUmJiYm -a ksdocker1

heroku container:push web -a ksdocker1 && heroku container:release web -a ksdocker1
```

- kuaishou2
```
xicela2706@dkb3.com

heroku login -i
heroku container:login
heroku create ksdocker2
heroku config:set ksmullive_idx=2 ksmullive_tot=10 cookies=ZGlkJiYmd2ViXzIwNzcxOTg0MTdhZWJmYmJjNDg5NDk0MzdiZmY3M2Y1JiYmJmNsaWVudGlkJiYmMyYmJiZjbGllbnRfa2V5JiYmNjU4OTBiMjkmJiYma3BuJiYmR0FNRV9aT05FJiYmJnVzZXJJZCYmJjY0NzQ0NjIxOCYmJiZrdWFpc2hvdS5saXZlLmJmYjFzJiYmYWM1ZjI3YjNiNjI4OTU4NTljNGMxNjIyZjQ5ODU2YTQmJiYmZGlkdiYmJjE2NDE5MTYxNTcwMDAmJiYma3VhaXNob3UubGl2ZS53ZWJfc3QmJiZDaFJyZFdGcGMyaHZkUzVzYVhabExuZGxZaTV6ZEJLZ0FlT1B6bjBJUERST0g5TEtqV01qbzhORDYzT2Z0M3E2TXBUZjRncmIyS0Q2YVhjRnJiVjJPLTZIMFRyWDZzLVl2cTBTNnBLcFk2VzRUcUl4VC12NWdPNWp1a0hfa2ItSXBvc1lUX3J0a2I5bWlQcmVvdDVKcWE1LTRpdFhCby1qTllZVVpTN1FGcGtsTEp6bzJFcFFJeV80RVJXQVNQbzBGbHczaVlYckZGa1Rob1loYWZJVVJCYWhOLWpXNTVJMjZ6UzdrSHV6c3c4UXh0S3Q5dFYyaXhvYUVnVnMxTlVHTmtobGk5ZVVBdmNKdENxTXNpSWdkNERSWFJ5UnJac1pSSEpLNnR3b2FVVjBJRDE2dWZJN1FzdFEybTlEYmZzb0JUQUImJiYma3VhaXNob3UubGl2ZS53ZWJfcGgmJiZhYTRjNjQ4YjMwNmVkODg3OTIwYjAzZmIxMmM0ODRkYmI4MDUmJiYm -a ksdocker2

heroku container:push web -a ksdocker2 && heroku container:release web -a ksdocker2
```

- kuaishou3
```
korage8234@huekieu.com

heroku login -i
heroku container:login
heroku create ksdocker3
heroku config:set ksmullive_idx=3 ksmullive_tot=10 cookies=ZGlkJiYmd2ViXzIwNzcxOTg0MTdhZWJmYmJjNDg5NDk0MzdiZmY3M2Y1JiYmJmNsaWVudGlkJiYmMyYmJiZjbGllbnRfa2V5JiYmNjU4OTBiMjkmJiYma3BuJiYmR0FNRV9aT05FJiYmJnVzZXJJZCYmJjY0NzQ0NjIxOCYmJiZrdWFpc2hvdS5saXZlLmJmYjFzJiYmYWM1ZjI3YjNiNjI4OTU4NTljNGMxNjIyZjQ5ODU2YTQmJiYmZGlkdiYmJjE2NDE5MTYxNTcwMDAmJiYma3VhaXNob3UubGl2ZS53ZWJfc3QmJiZDaFJyZFdGcGMyaHZkUzVzYVhabExuZGxZaTV6ZEJLZ0FlT1B6bjBJUERST0g5TEtqV01qbzhORDYzT2Z0M3E2TXBUZjRncmIyS0Q2YVhjRnJiVjJPLTZIMFRyWDZzLVl2cTBTNnBLcFk2VzRUcUl4VC12NWdPNWp1a0hfa2ItSXBvc1lUX3J0a2I5bWlQcmVvdDVKcWE1LTRpdFhCby1qTllZVVpTN1FGcGtsTEp6bzJFcFFJeV80RVJXQVNQbzBGbHczaVlYckZGa1Rob1loYWZJVVJCYWhOLWpXNTVJMjZ6UzdrSHV6c3c4UXh0S3Q5dFYyaXhvYUVnVnMxTlVHTmtobGk5ZVVBdmNKdENxTXNpSWdkNERSWFJ5UnJac1pSSEpLNnR3b2FVVjBJRDE2dWZJN1FzdFEybTlEYmZzb0JUQUImJiYma3VhaXNob3UubGl2ZS53ZWJfcGgmJiZhYTRjNjQ4YjMwNmVkODg3OTIwYjAzZmIxMmM0ODRkYmI4MDUmJiYm -a ksdocker3

heroku container:push web -a ksdocker3 && heroku container:release web -a ksdocker3
```

- kuaishou4
```
weledix411@liepaia.com
Yttyhxways778!

heroku login -i
heroku container:login
heroku create ksdocker4
heroku config:set ksmullive_idx=4 -a ksdocker4
git add -A && git commit -m "add kuaishou4" && git push origin kuaishou4
heroku container:push web -a ksdocker4 && heroku container:release web -a ksdocker4
```