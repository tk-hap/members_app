FROM python:3.11-alpine

WORKDIR /app

COPY members_app/requirements.txt /app

RUN pip install -r requirements.txt --no-cache-dir

COPY members_app/. /app

RUN chmod +x /app/bin/app