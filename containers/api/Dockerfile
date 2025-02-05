FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN mkdir /api

WORKDIR /api

COPY ./requirements.txt /api

RUN pip install --upgrade pip && pip install -r requirements.txt

ADD . /api/