FROM python:3.7-slim

MAINTAINER "pratap.varu@gmail.com"

ENV PYTHONUNBUFFERED 1

RUN mkdir /ghilib_studio
WORKDIR /ghilib_studio

COPY . /ghilib_studio/
RUN pwd

RUN export DJANGO_SETTINGS_MODULE=ghibli_studio.settings

RUN pip install -r requirements.txt