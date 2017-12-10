# -*- coding: utf-8 -*-
import scrapy
import sys
from Bili.items import BiliItem 
import copy
class BilibiliSpider(scrapy.Spider):
    name = 'bilibili'
    allowed_domains = ['www.bilibili.com']
    start_urls = ['https://search.bilibili.com/all?keyword=bixby&page=1&order=totalrank']

    def parse(self, response):
        num_pages = int(response.xpath('//body/@data-num_pages').extract_first())
        cur_page = int(response.xpath('//body/@data-cur_page').extract_first())
        item = BiliItem()
        for line  in response.xpath("//li[@class='video matrix ']"):
            item['title'] = line.xpath("./a/@title").extract()[0]
            item['url'] = 'https:'+line.xpath("./a/@href").extract()[0]
            item['createtime'] = line.xpath(".//span[@class='so-icon time']").xpath('string(.)').extract()[0]
            #ll = copy.deepcopy(item)
            print(item['url'])
            #yield scrapy.Request(item['url'],callback=self.parse_comment,dont_filter = True)
            yield scrapy.Request(item['url'],meta={'item':copy.deepcopy(item)},callback=self.parse_comment,dont_filter = True)
            #scrapy.Request.meta['item'] = ''
        if cur_page >=num_pages:
            pass 
        next_page = 'https://search.bilibili.com/all?keyword=bixby&page={i}&order=totalrank'.format(i=cur_page+1)
        yield scrapy.Request(next_page,callback=self.parse,dont_filter = True)   
    def parse_comment(self,response):
        print('*'*40)
        print(response.url)
        print(response.meta['item']['url'])
        #oid = int(response.xpath("//span[@class='t fav_btn']/@href").extract_first()[-8:])
        #url = 'https://api.bilibili.com/x/v2/reply?&jsonp=jsonp&pn=1&type=1&oid={oid}&sort=0'.format(oid=oid)
        #yield scrapy.Request(item['url'],callback=self.get_comment,meta=meta,dont_filter = True)
    #def get_comment(self,response):
    #    pass
