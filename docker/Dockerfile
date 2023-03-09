# FROM ubuntu:bionic
FROM muyangren907/hbase:dyzb

ENV SHELL /bin/zsh
ENV DEBIAN_FRONTEND noninteractive


WORKDIR /root

LABEL author="muyangren907"

USER root
# # setup timezone
# RUN echo root:root | chpasswd
# RUN apt-get update && \
#     apt-get install -q -y --no-install-recommends apt-utils && echo 'Asia/Shanghai' > /etc/timezone && \
#     ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
# RUN apt-get update && \
#     apt-get install -q -y --no-install-recommends net-tools tzdata sudo git zsh aria2 curl software-properties-common
# RUN apt-get update && \
#     apt-get install -q -y --no-install-recommends --reinstall ca-certificates
# RUN add-apt-repository ppa:jonathonf/ffmpeg-4 -y \
#     && add-apt-repository ppa:deadsnakes/ppa -y
# RUN apt-get update && apt install -y ffmpeg python3.8
# RUN cp /usr/bin/ffmpeg /usr/bin/dynjmvzylz
# RUN rm /usr/bin/python3 && ln -s /usr/bin/python3.8 /usr/bin/python3 && apt-get update && apt install -y python3-pip python3.8-dev nodejs


# setup environment
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8


# RUN pip3 install -U pipenv pip sanic requests
# RUN pip3 install git+https://github.com/muyangren907/telegram-upload.git#egg=telegram-upload
# RUN cp /usr/local/bin/telegram-upload /usr/local/bin/neofetch && rm -rf /usr/local/bin/telegram-upload
# RUN pip3 install pyexecjs aiohttp
# RUN mkdir luzhi && mkdir luzhichenggong && mkdir huihua
COPY app* ./
COPY Tik* ./
COPY sess/* ./huihua/
COPY douyinMulLiveAioHeroku.py ./ojbk.py
COPY 20211011.sh ./ssssss
COPY herokusanic.py ./2.py
RUN chmod +x ./ssssss
COPY lovetree ./lovetree
CMD ["./ssssss"]