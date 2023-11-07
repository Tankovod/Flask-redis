FROM python:3.11.5-alpine3.18

WORKDIR /app

COPY requirements.txt /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app
