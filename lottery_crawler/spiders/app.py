# -*- coding: utf-8 -*-
""" This is to define the encoding """
import scrapy
from scrapy import Selector
from scrapy import Request

class NgaSpider(scrapy.Spider):
    """ This is the class of the Spider """
    name = "NgaSpider"
    #host = "http://bbs.ngacn.cc/"
    allowed_domains = ["www.cnblogs.com"]

    start_urls = [
        "http://www.cnblogs.com/txw1958/archive/2012/07/16/scrapy-tutorial.html"
    ]

    def parse(self, response):
        hxs = Selector(response)
        title = hxs.xpath('//*[@id="cb_post_title_url"]/text()').extract() 
        link = hxs.xpath('//*[@id="cb_post_title_url"]/@href').extract()      
        for t in title:
            print t.encode('utf-8')
