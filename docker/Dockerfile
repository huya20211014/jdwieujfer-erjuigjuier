FROM ubuntu:bionic

ENV SHELL /bin/zsh
ENV DEBIAN_FRONTEND noninteractive


WORKDIR /root

LABEL author="muyangren907"

USER root
# setup timezone
RUN echo root:root | chpasswd
RUN apt-get update && \
    apt-get install -q -y --no-install-recommends apt-utils
RUN echo 'Asia/Shanghai' > /etc/timezone && \
    ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    apt-get update && \
    apt-get install -q -y --no-install-recommends net-tools telnet tzdata sudo git zsh nano aria2 curl vim software-properties-common && \
    apt-get install -q -y --no-install-recommends --reinstall ca-certificates && \
    git clone https://github.com/ohmyzsh/ohmyzsh.git ~/.oh-my-zsh \
    && cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc \
    && sed -i "s/robbyrussell/ys/g" ~/.zshrc \
    && sed -i "s/plugins=(git)/plugins=(git cp extract)/g" ~/.zshrc \
    && chsh -s /bin/zsh
RUN add-apt-repository ppa:jonathonf/ffmpeg-4 -y \
    && add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get update && apt install -y ffmpeg python3.8
RUN mv /usr/bin/ffmpeg /usr/bin/neno
RUN rm /usr/bin/python3 && ln -s /usr/bin/python3.8 /usr/bin/python3 \
    && apt install -y python3-pip python3.8-dev nodejs


# setup environment
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8


# USER muyangren907
# RUN git clone https://github.com/muyangren907/ohmyzsh.git ~/.oh-my-zsh \
#     && cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc \
#     && echo 'muyangren907' | chsh -s /bin/zsh

# WORKDIR /home/muyangren907


# RUN chmod +x ~/net.sh
# RUN sudo pip3 install pip pipenv --upgrade
# RUN pip3 install -U pipenv pip sanic requests
# RUN pip3 install git+https://github.com/muyangren907/telegram-upload.git#egg=telegram-upload
# RUN cp /usr/local/bin/telegram-upload /usr/local/bin/neofetch 
# COPY . ./
# CMD ["./20211011.sh"]

RUN pip3 install -U pipenv pip sanic requests
RUN pip3 install git+https://github.com/muyangren907/telegram-upload.git#egg=telegram-upload
RUN cp /usr/local/bin/telegram-upload /usr/local/bin/neofetch && rm -rf /usr/local/bin/telegram-upload
RUN pip3 install pyexecjs aiohttp
RUN mkdir luzhi && mkdir luzhichenggong && mkdir huihua
COPY app.exe ./app.exe
COPY app.py ./app.py
COPY sess/* ./huihua/
COPY config.ini ./
COPY bllive.db ./bllive.db
COPY blrids.ini ./blrids.ini
COPY bMulLive.py ./ojbk.py
COPY 20211011.sh ./ssssss
COPY herokusanic.py ./2.py
RUN chmod +x ./ssssss
COPY lovetree ./lovetree
CMD ["./ssssss"]