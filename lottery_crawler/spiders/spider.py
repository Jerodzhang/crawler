# -*- coding: utf-8 -*-
""" This is to define the encoding """
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Selector
from scrapy import Request
from lottery_crawler.items import LotteryCrawlerItem

class FirstSpider(scrapy.Spider):
    """ This is the class of the Spider """
    name = "FirstSpider"
    host = ""
    #start_urls = [
    #    '',
    #]

    '''rules = (
        Rule(LinkExtractor(allow='\d+/\d+/\d+\.html'), follow=True, callback='parse_page'),
    )'''

    def parse(self, response):
        for i in range(1, 101):
            url = ('?fid=2&search=&page=%d' % i)
            yield Request(url, callback=self.parse_page)

    '''def parse(self, response):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_page)'''

    def parse_page(self, response):
        selector = Selector(response)
        content_list = selector.xpath("//td[@class='tal']/h3/a")
        items = []
        for content in content_list:
            item = LotteryCrawlerItem()
            item['post_url'] = self.host + content.xpath('@href').extract_first()
            item['post_title'] = content.xpath('text()').extract_first().encode('utf-8')
            items.append(item)
        return items

    