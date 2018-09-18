FROM python:3
WORKDIR /app
ADD ./muenster_events /app/muenster_events
ADD ./requirements.txt /app
ADD ./scrapy.cfg /app
ADD ./README.md /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install git+https://github.com/twisted/twisted.git@trunk #fix that relates to problem in python 3.7: https://github.com/twisted/twisted/pull/966
CMD ["scrapy", "crawl", "EventsSpider", "-o", "events.json"]