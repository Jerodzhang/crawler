# -*- coding: utf-8 -*-
""" This is to define the encoding """
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
from scrapy.selector import Selector
from scrapy.http import Request
from lottery_crawler.items import LotteryCrawlerItem

class NgaSpider(scrapy.Spider):
    """ This is the class of the Spider """
    name = "NgaSpider"
    #host = "http://bbs.ngacn.cc/"
    allowed_domains = ["dmoztools.net"]

    start_urls = [2,4]

    rules = (
        Rule(LinkExtractor(allow='\d+/\d+/\d+\.html'), follow=True, callback='get_torrent'),
    )

    def start_requests(self):
        for url_id in self.start_urls:
            yield Request('?fid=%d' % url_id)
            for i in range(2, 101):
                yield Request('?fid=%d&search=&page=%d' % (url_id, i))

    def parse_item(self, response):
        item = LotteryCrawlerItem()
        item['post_title'] = response.meta['cl_title']
        item['post_url'] = response.meta['cl_url']
        item['post_bankuai'] = response.meta['cl_bankuai']
        item['posted'] = response.meta['posted']
        sel = Selector(response)
        downloaded = sel.xpath('//td/table/tr/td/text()').extract()[2]
        item['torrent_downloaded'] = downloaded[17:]
        item['torrent_url'] = response.url
        ref = sel.xpath('//input[@name="ref"]/@value').extract_first()
        reff = sel.xpath('//input[@name="reff"]/@value').extract_first()

        dl = ('http://www.rmdown.com/download.php?ref=%s&&reff=%s&submit=download' % (ref, reff)).encode('utf-8')
        item['torrent_download_urls'] = dl

        yield item

    def get_torrent(self, response):
        sel = Selector(response)
        cl_title = sel.xpath('//td[@class="h"]/text()[2]').extract_first()
        cl_bankuai = sel.xpath('//div[@class="t3"]/table/tr/td/b/a[2]/text()').extract_first()
        cl_url = response.url
        torrent = re.search('rmdown\.com(.+?)</a>', response.body)
        torrent_url = 'http://www.' + torrent.group()[:-4]
        posted = sel.xpath('//div[@class="tipad"]/text()').extract()[1]
        posted = posted.encode('utf-8')[9:-7]
        yield Request(
            url=torrent_url,
            meta={
                'cl_title': cl_title,
                'cl_bankuai': cl_bankuai,
                'cl_url': cl_url,
                'posted': posted,
            },
            callback=self.parse_item,
            dont_filter=True)
