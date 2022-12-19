FROM python:3.9.10-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean \
    && /usr/local/bin/python -m pip install --upgrade pip \
    && apt-get install -y default-libmysqlclient-dev

RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /app/