# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    #allowed_domains = ['example.com']
    #start_urls = ['http://example.com/']
   # def parse(self, response):
   #     #pass
   #     page = response.url.split("/")[-2]
   #     filename = 'quotes-%s.html' % page
   #     with open(filename, 'wb') as f:
   #         f.write(response.body)
   #     self.log('Saved file %s' % filename)
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
