﻿# MS-Event-Scrapy
This Scrapy-project can be used to extract event information from the event calendar of the city of Münster.

## Dependencies and installation
The only dependency of this project is Scrapy itself. See the official documentation to see how it is installed:
https://docs.scrapy.org/en/latest/intro/install.html

## Usage
To run the crawler and write the results into the file events.json use:

   scrapy crawl EventsSpider -o events.json

This will return today's events from Muenster's event calendar by default. You can also specify a start and end date:

   scrapy crawl EventsSpider -o events.json -a start=26.07.2018 -a end=05.08.2018

The start and end date must be in format DD.MM.YYYY, including trailing zeroes.

The following is also allowed, but can be left away. The end date will be ignored if given.

    scrapy crawl EventsSpider -o events.json -a start=today

## Result format

See this example
```
{
  "title": "Herr Roberz liest: Bauer Beck f\u00e4hrt weg",
  "subtitle": "F\u00fcr Kinder ab 4 Jahren, Eintritt frei",
  "start_date": "2018-07-26T16:30:00",
  "end_date": "2018-07-26T17:30:00",
  "location": "B\u00fccherei am Hansaplatz",
  "location_addresse": "Wolbecker Stra\u00dfe 97",
  "description": "\"Ein Bauer f\u00e4hrt nicht in den Urlaub\", denkt Bauer Beck, bis eines Tages die Magd Toni ans Meer f\u00e4hrt. Was die Magd kann, kann er auch. Kurzerhand schnappt er seine Tiere und f\u00e4hrt los ...",
  "link": "http://www.stadt-muenster.de/buecherei/veranstaltungen/",
  "category": "Kabarett, Lesungen, Comedy"
}
```
If the end time was not given end_date will be empty. The start_date might also not contain a time if it was not given. Notice the escaped unicode characters: this is the standard behavior of Scrapy's JSON exporter.