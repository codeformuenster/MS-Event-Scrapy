# MS-Event-Scrapy
This Scrapy-project can be used to extract event information from the event calendar of the city of Münster.

## Dependencies and installation
The only mandatory dependency of this project is Scrapy itself. See the official documentation to see how it is installed:
https://docs.scrapy.org/en/latest/intro/install.html

## Usage
To run the crawler and write the results into the file events.json use:

    scrapy crawl EventsSpider -o events.json

This will return events of the next year from Muenster's event calendar by default. You can also specify a start and end date:

    scrapy crawl EventsSpider -o events.json -a start=26.07.2018 -a end=05.08.2018

The start and end date must be in format DD.MM.YYYY, including trailing zeroes.

The following is also allowed, but can be left away. The end date will be ignored if given.

    scrapy crawl EventsSpider -o events.json -a start=today

The parameter always takes precedence over the environment variable.

## Result format

See this example
```
{
    "title": "Lesung: Des Kaisers neue Kleider",
    "subtitle": "F\u00fcr Kinder ab 4 Jahren, Eintritt frei",
    "start_date": "2018-11-08T15:00:00",
    "end_date": "2018-11-08T15:40:00",
    "location": "B\u00fccherei Kinderhaus",
    "location_addresse": "Idenbrockplatz 8",
    "description": "Lesung anl\u00e4sslich der M\u00fcnsteraner M\u00e4rchenwochen. Betr\u00fcger schw\u00e4tzen dem eitlen Kaiser ein prachtvolles Gewand auf, das er stolz seinen Untertanen vorf\u00fchrt. \u00dcberrascht klatschen sie Beifall, bis ein Kind ausspricht, was alle erkannt haben: Der Kaiser ist ja nackt!",
    "link": "http://www.stadt-muenster.de/buecherei/veranstaltungen/fuer-kinder.html",
    "category": "Kabarett, Lesungen, Comedy",
    "pos": "1054218112018"
}
```
If the end time was not given end_date will be empty. The start_date might also not contain a time if it was not given. Notice the escaped unicode characters: this is the standard behavior of Scrapy's JSON exporter.
