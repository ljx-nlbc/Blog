#基础镜像
FROM python:3.13-slim

#容器工作路径
WORKDIR /app

#安装依赖
RUN apt-get update \
&& apt-get install -y  --no-install-recommends\
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
&& rm -rf /var/lib/apt/lists/* \
&& apt-get clean

#复制requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

#宿主机内的东西拷贝到容器中
COPY . .

#运行
CMD [ "python","manage.py","runserver","0.0.0.0:8000"]