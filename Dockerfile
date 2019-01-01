FROM python:3.7-alpine
WORKDIR /usr/src/app
COPY ./muenster_events /usr/src/app/muenster_events
COPY ./requirements.txt /usr/src/app/
COPY ./scrapy.cfg /usr/src/app/
COPY ./README.md /usr/src/app/
RUN apk add musl-dev gcc linux-headers libxml2-dev libffi-dev openssl-dev libxslt-dev zlib-dev
RUN pip install -r requirements.txt
RUN mkdir data
CMD ["scrapy", "crawl", "EventsSpider", "-o", "data/result.jsonl", "-t", "jsonlines"]
