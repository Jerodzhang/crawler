# -*- coding: utf-8 -*-
""" This is to define the encoding """
import scrapy
from scrapy import Selector
from scrapy import Request

class NgaSpider(scrapy.Spider):
    """ This is the class of the Spider """
    name = "NgaSpider"
    host = "http://bbs.ngacn.cc/"

    start_urls = [
        "http://bbs.ngacn.cc/thread.php?fid=406"
    ]

    def parse(self, response):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        selector = Selector(response)
        content_list = selector.xpath("//*[@class='topic']")
        for content in content_list:
            topic = content.xpath('string(.)').extract_first()
            print(topic)

            url = self.host + content.xpath('@href').extract_first()
            print(url)
            yield Request(url=url, callback=self.parse_topic)

    def parse_topic(self, response):
        selector = Selector(response)
        content_list = selector.xpath("//*[@class='postcontent ubbcode']")
        for content in content_list:
            content = content.xpath('string(.)').extract_first()
            print(content)
