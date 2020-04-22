# -*- coding: utf-8 -*-
import scrapy
from dytt.items import DyttItem
import logging
class DyttSpider(scrapy.Spider):
    name = 'Dytt'
    allowed_domains = ['www.dytt8.net']
    start_urls = ['https://www.dytt8.net/html/gndy/index.html']

    def parse(self, response):
        item=DyttItem()
        more=response.xpath('//div[@class="co_area2"]/div[1]/p[1]/em/a/@href').getall()
        for i in more:
            item['url']='https://www.dytt8.net'+i
            logging.info('url is: %s'%item['url'])
            yield scrapy.Request(item['url'],callback=self.more_parse,meta={'item':item,'more_url':item['url']})

    def more_parse(self,response):
        item=response.meta['item']
        front_url=response.url
        #print(front_url)
        front_url=front_url[:-10]
        #print(response.text)
        item['title']=response.xpath('//div[@class="co_content8"]//table[@class="tbspan"]/tr[2]/td[2]/b/a/text()').getall()
        item['next_url']=[]
        urls=response.xpath('//div[@class="co_content8"]//table[@class="tbspan"]/tr[2]/td[2]/b/a/@href').getall()
        try:
            next_page=response.xpath('//div[@class="co_content8"]/div/td/a[7]/@href').get()
            next_page_url=front_url+next_page
            #print(next_page_url)
        except Exception as e:
            print(e)
        if next_page_url:
            yield scrapy.Request(next_page_url,callback=self.more_parse,meta={"item":item})

        for i in urls:
            i='https://www.dytt8.net'+i
            item['next_url'].append(i)
        #print(item['title'])

            print(item['next_url'])
            yield scrapy.Request(i,callback=self.detail_parse,meta={'item':item})
    def detail_parse(self,response):
        item=response.meta['item']
        item['movie_url']=response.xpath('//div[@id="Zoom"]//table//tr[1]/td[1]/a/@href').getall()

        #print(item['movie_url'])
        return item