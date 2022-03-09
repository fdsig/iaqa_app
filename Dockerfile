# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /

COPY requirements.txt requirements.txt 

RUN pip install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y python3-opencv

COPY . .

CMD ["python3", "app.py"]


