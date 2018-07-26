# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime

class EventsSpider(scrapy.Spider):
    name = 'EventsSpider'
    allowed_domains = ['muenster.de']
    start_url = 'https://www.muenster.de/veranstaltungskalender/scripts/frontend/suche.php'
    
    def start_requests(self):
        req_start_date = getattr(self, 'start', None)
        req_end_date = getattr(self, 'end', None)
        
        if(req_start_date is None):
            req_start_date = 'today'
        else:
            if(req_start_date is not 'today' and req_end_date is None):
                self.log('End date not given, using "today" as start date.')
                req_start_date = 'today'
        
        # TODO: validate start/end date
        
        yield scrapy.Request(self.start_url, self.parse, meta={'req_start_date' : req_start_date, 'req_end_date' : req_end_date})

    def parse(self, response):
        """Submit the search form searching for events that start today."""
        
        datum_von = ''
        datum_bis = ''
        zeitraum = ''
        
        if(response.meta['req_start_date'] is None or response.meta['req_start_date'] is 'today'):
            zeitraum = 'heute'
        else:
            datum_von = response.meta['req_start_date']
            datum_bis = response.meta['req_end_date']
            zeitraum = 'zeitraum'
        
        return scrapy.FormRequest.from_response(
                response,
                formname='submit',
                formdata={'datum_bis': datum_bis, 'datum_von': datum_von, 'submit': 'Suchen', 'suchstring': '', 'volltextsuche-verknuepfung': 'und', 'zeitraum': zeitraum, 'zielgruppe': 'alle'},
                callback=self.after_post
            )

    
    def after_post(self, response):
        """Response here is the overview page over all events. We collect the links to the individual detail pages."""
        
        detail_links = response.xpath("//a[text() = 'Details']/@href").extract();
        for href in detail_links:
            categories = response.xpath("//a[@href = '" + href + "']/ancestor::div[@class = 'eintrag ']/preceding-sibling::div[@class = 'kategorie']/text()").extract();
            category = categories[-1]; #select the last of all preceding categories
            if(category is not None):
                category = category.strip(' \t\n\r')
            yield response.follow(href, callback=self.extract_event, meta = {'category':category})
            
    def getText(self, response, clazz):
        """Find the first div with the class clazz and extract the text, stripping whitespaces and such."""
        
        return response.xpath("//div[@class='" + clazz + "']/text()").extract_first().strip(' \t\n\r')
    
    def produce_dates(self, raw_datetime):
        """ Try to produce a clean start and end date (if it exists)."""
        
        # dates are usually of format "Donnerstag, 26.7.2018, 21.30 - 23.30 Uhr"
        # if there is only a start time it's just "Donnerstag, 26.7.2018, 21.30 Uhr"
        # sometimes the time is missing entirely, then it's just "Donnerstag, 26.7.2018,"
        # we'll ignore the leading day of the week
        
        datetime_parts = raw_datetime.split(',') # split at commas
        date = datetime_parts[1].strip(' \t\n\r') # drop whitespaces and such
        start_time = ''
        end_time = ''
        if(len(datetime_parts) > 2): # if there is a time given
            time = datetime_parts[2].replace('Uhr', '') # drop unnessary string
            time_splits = time.split('-') # split start and end time
            start_time = time_splits[0].strip(' \t\n\r') 
            
            if(len(time_splits) > 1):
                end_time = time_splits[1].strip(' \t\n\r')
                
        start_date = ''
        end_date = ''
                
        # produce proper ISO conform datetime strings
        if(start_time is ''):
            start_date = datetime.strptime(date, '%d.%m.%Y') # case: no time
        else:
            start_date = datetime.strptime(date + ' ' + start_time, '%d.%m.%Y %H.%M').isoformat()
            
        if(end_time is not ''):
            end_date = datetime.strptime(date + ' ' + end_time, '%d.%m.%Y %H.%M').isoformat()
        
        return (start_date, end_date)
    
    def extract_event(self, response):
        """Callback function for the detail pages. We find the indivudal data points and try to bring the date/time in proper form, then
        summarize it into a Event-object and return it."""
        
        # extract the interesting data points
        title = self.getText(response, 'titel')
        subtitle = self.getText(response, 'untertitel')
        raw_datetime = self.getText(response, 'datum-uhrzeit')
        description = self.getText(response, 'detailbeschreibung')
        location = self.getText(response, 'location')
        location_adresse = self.getText(response, 'location-adresse')
        link = response.xpath("//div[@class='detail-link']/a/@href").extract_first().strip(' \t\n\r')
        
        times = self.produce_dates(raw_datetime);
        start_date = times[0]
        end_date = times[1]
       
        
        return Event(title = title, 
              subtitle = subtitle, 
              start_date = start_date, 
              end_date = end_date, 
              location = location, 
              location_addresse = location_adresse, 
              description = description, 
              link = link,
              category = response.meta['category']
          )
        
        
class Event(scrapy.Item):
    title = scrapy.Field()
    subtitle = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    location = scrapy.Field()
    location_addresse = scrapy.Field()
    description = scrapy.Field()
    link = scrapy.Field()
    category = scrapy.Field()