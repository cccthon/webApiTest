FROM python

WORKDIR /opt

COPY requirements.txt ./
RUN mkdir -p /root/.pip&&echo "[global]" > /root/.pip/pip.conf&&echo "index-url = https://pypi.tuna.tsinghua.edu.cn/simple">> /root/.pip/pip.conf

RUN echo "deb http://mirrors.ustc.edu.cn/debian jessie main contrib non-free"> /etc/apt/sources.list
RUN echo "deb-src http://mirrors.ustc.edu.cn/debian jessie main contrib non-free">> /etc/apt/sources.list
RUN echo "deb http://mirrors.ustc.edu.cn/debian jessie-proposed-updates main contrib non-free">> /etc/apt/sources.list
RUN echo "deb-src http://mirrors.ustc.edu.cn/debian jessie-proposed-updates main contrib non-free ">> /etc/apt/sources.list
RUN echo "deb http://mirrors.ustc.edu.cn/debian jessie-updates main contrib non-free">> /etc/apt/sources.list
RUN echo "deb-src http://mirrors.ustc.edu.cn/debian jessie-updates main contrib non-free">> /etc/apt/sources.list

RUN TZ=Asia/Shanghai&&ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
#COPY sources.list /etc/apt/
RUN apt-get update && apt-get install -y freetds-dev
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./your-daemon-or-script.py" ]