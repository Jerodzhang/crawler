# -*- coding: utf-8 -*-
""" This is to define the encoding """
import scrapy
from scrapy import Selector
from scrapy import Request
from lottery_crawler.items import LotteryCrawlerItem

class NgaSpider(scrapy.Spider):
    """ This is the class of the Spider """
    name = "NgaSpider"
    #host = "http://bbs.ngacn.cc/"
    allowed_domains = ["dmoztools.net"]

    start_urls = [
        "http://dmoztools.net/Computers/Programming/Languages/Python/Books/"
    ]

    def parse(self, response):
        hxs = Selector(response)
        #title = hxs.xpath('//*[@id="cb_post_title_url"]/text()').extract() 
        #link = hxs.xpath('//*[@id="cb_post_title_url"]/@href').extract()      
        ''' for t in title:
            print t.encode('utf-8') '''
        ''' print "URL: "
        for l in link:
            print l.encode('utf-8') '''
        sites = hxs.xpath('//*[@class="title-and-desc"]')
        items = []
        for site in sites:            
            item = LotteryCrawlerItem()
            item['title'] = site.xpath('a/div/text()').extract()
            item['link'] = site.xpath('a/@href').extract()
            item['desc'] = site.xpath('div/text()').extract()
            items.append(item)
        return items
            #print "desc: " 
            #print desc
