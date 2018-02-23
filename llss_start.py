#!/usr/bin/env python3
#-*-coding:utf-8-*-

import scrapy
import os
import re
import pipelines
from llss_items import LlssAllItem
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import fake_useragent
import copy

ua = fake_useragent.UserAgent()


'''
defination of the two spiders
the first is used to get the url to start with
the second is the main one
'''
class llss_all_pre_spider(scrapy.Spider):
    name = 'llss_all_pre'
    start_urls = [
        'https://www.llss.fun/wp/',
    ]
    def parse(self,response):
        page = response.xpath('//h1[@class="entry-title"]/a/@href').extract_first()
        path = './config/start_urls.txt'
        with open(path,'w') as f:
            f.write(page)


class llss_all_spider(scrapy.Spider):
    name = 'llss_all'
    custom_settings = {
        'TELNETCONSOLE_ENABLED' : False,
        'USER_AGENT': ua.random,
        'COOKIES_ENABLED' : False,
        'ITEM_PIPELINES': {
            'pipelines.LlssAll_abstrct_Pipeline': 1,
            'pipelines.LlssAll_image_Pipeline': 2,
            },
        }
    S = []
    if os.path.isfile('./config/start_urls.txt'):
        with open('./config/start_urls.txt') as file:
            S.append(file.read())
    start_urls = S

    def date_check(self, date_to_check, date_stop):
        if date_to_check < date_stop:
            return 0
        else:
            return 1

    def parse(self,response):
        date_stop = ''
        with open('./config/date_stop.txt') as f:
            t = f.readline()
            date_stop = t[0:4] + t[5:7] + t[8:10]
            date_stop = int(date_stop)
        item = LlssAllItem()
        for content in response.xpath('//body'):
            item['title'] = content.xpath('//h1[@class="entry-title"]/text()').extract_first()
            tmp_date = content.xpath('//body//time[@class="entry-date"]/@datetime').extract_first()
            date = tmp_date[0:4] + tmp_date[5:7] + tmp_date[8:10]
            item['post_date'] = int(date)
            item['abstract'] = (content.xpath('//div[@class="entry-content"]/*/text()|'
                                              '//div[@class="entry-content"]/*/*/text()').extract())
            M1 = (content.xpath('//div[@class="entry-content"]/*/text()|//div[@class="entry-content"]/*/*/'
                                'text()').re('([0-9a-fA-F]+)本站不提供下载([0-9a-fA-F]+)'))
            M1 += (content.xpath('//div[@class="entry-content"]/*/*/*/*/text()|//div[@class="entry-content"]/*/*/*/'
                                'text()').re('([0-9a-fA-F]+)本站不提供下载([0-9a-fA-F]+)'))
            M2 = (content.xpath('//div[@class="entry-content"]/*/text()|'
                                '//div[@class="entry-content"]/*/*/text()').re('.*[0-9a-zA-Z]{15,}'))
            M2 += (content.xpath('//div[@class="entry-content"]/*/*/*/text()|'
                                '//div[@class="entry-content"]/*/*/*/*/text()').re('.*[0-9a-zA-Z]{15,}'))
            M3 = (content.xpath('//div[@class="entry-content"]/*/text()'
                                '|//div[@class="entry-content"]/*/*/text()').re('magnet:\?xt=urn:btih:[0-9a-fA-F]+'))
            M3 += (content.xpath('//div[@class="entry-content"]/*/*/*/text()'
                                '|//div[@class="entry-content"]/*/*/*/*/text()').re('magnet:\?xt=urn:btih:[0-9a-fA-F]+'))
            i = 0
            while i < len(M1):
                tmp=M[i]+M[i+1]
                M2.append(copy.copy(tmp))
                tmp.clear()
                i+=2
            item['magnet_without_prefix'] = M2
            item['magnet_with_prefix'] = M3
            item['image_urls'] = content.xpath('//div[@class="entry-content"]//img/@src').extract()
            image_type = []
            for url in item['image_urls']:
                for i in range(1, 7):
                    if url[-i] == '.':
                        break
                    i += 1
                image_type.append(url[-i:])
            item['image_type'] = image_type
            next_page = response.xpath('//div[@id="content"]//span[@class="nav-previous"]/a/@href').extract_first()
        print(item['post_date'],'==>',date_stop)
        yield item
        if next_page is not None:
            if self.date_check(item['post_date'], date_stop) == 1:
                yield response.follow(next_page, callback=self.parse)
        return item

if __name__=='__main__':
    print('detecting configure')
    if not os.path.isdir('./config/'):
        print('no configure file,creating one')
        os.mkdir('./config/')
    stop = input('please input the date to stop in format as YYYY/MM/DD: ')
    with open('./config/date_stop.txt','w') as f:
        f.write(stop)

    #run the two spiders sequencely
    configure_logging()
    runner = CrawlerRunner()
    @defer.inlineCallbacks

    def crawl():
        yield runner.crawl(llss_all_pre_spider)
        yield runner.crawl(llss_all_spider)
        reactor.stop()

    crawl()
    reactor.run()

    '''
    pause to check results.
    on unix system python scripts usally run in a terminal,so the is no need to pause.
    '''
    if os.name == 'nt':
        os.system('pause')
