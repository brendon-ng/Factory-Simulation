FROM python:3.8.0-slim-buster

COPY requirements.txt /requirements.txt

RUN apt-get update && apt-get -y dist-upgrade

RUN apt-get -y install apt-utils \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    python3-pip \
    python3-numpy \
    python3-pandas

RUN pip install Cython
RUN pip install -r /requirements.txt

