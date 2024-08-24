FROM python

RUN apt-get update
RUN pip install scrapy
RUN pip install requests
RUN pip install beautifulsoup4

WORKDIR /app

COPY . /app