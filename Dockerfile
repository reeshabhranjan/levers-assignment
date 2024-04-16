FROM python:3.12-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install dependencies
RUN apk --no-cache add build-base libffi-dev
RUN apk add --upgrade --no-cache build-base linux-headers libcurl
RUN apk add --no-cache --virtual .build-dependencies build-base curl-dev
RUN apk add --no-cache --upgrade bash

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN apk del .build-dependencies

COPY . /app/

RUN sed -i 's/\r$//g' /app/start.sh
RUN chmod +x /app/start.sh

RUN addgroup -g 1000 -S appgroup
RUN adduser -D -u 1000 -G appgroup appuser
USER 1000:1000