FROM python:3.11-alpine

RUN apk add --no-cache bash

WORKDIR /app

COPY members_app/requirements.txt /app

RUN pip install -r requirements.txt --no-cache-dir

COPY members_app/. /app

RUN python manage.py collectstatic --clear --noinput

RUN chmod +x /app/bin/app && chmod +x /app/bin/waitfordb