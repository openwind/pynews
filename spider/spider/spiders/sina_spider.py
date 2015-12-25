# -*- coding : utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as sle
from scrapy.selector import Selector
from spider.items import SpiderItem
import urllib2
import string
import json
import re

class SinaSpider(CrawlSpider):
    name = "sinaspider"
    allowed_domains = ["news.sina.com.cn"]
    start_urls = [
        "http://news.sina.com.cn/"
            ]
    rules = [
        Rule(sle(allow = ('[0-9]\.shtml$',)), callback = 'parse_home', process_request = 'add_cookie'),
        Rule(sle(allow = ('/$',)), follow = True, process_request = 'add_cookie'),
        ]

    def add_cookie(self, request):
        request.replace(cookies = [
            {'name':'COOKIE_NAME', 'value':'VALUE', 'domain':'news.sina.com.cn', 'path':'/'},
            ])
        return request

    def parse_home(self, response):
        item = SpiderItem()

        item['Html'] = response.xpath("//html").extract()
        item['Source'] = 'sina'
        item['URL'] = response.url
        item['Time'] = response.url.split('/')[5]

        try:
            content_id = response.xpath("//head/meta[@name='comment']/@content").extract()
            news_id = "".join(content_id)
            item['ID'] = news_id[3:]
            item['Channel'] = news_id[:2]
        except:
            item['ID'] = "NULL"
            item['Channel'] = "NULL"
        #try:
        #    time = sel.xpath("//span[@id='pub_date']/text()").extract
        #    item['Time'] = time[0]
        #except:
        #    item['Time'] = 'NULL'
        try:
            words = response.xpath("//head/meta[@name='tags']/@content").extract()
            item['Keyword'] = ",".join(words)
        except:
            item['Keyword'] = 'NULL'
        try:
            str1 = 'http://comment5.news.sina.com.cn/page/info?format=json&channel='
            str2 = '&newsid='
            str3 = '&group=0&compress=1&ie=gbk&oe=gbk&page=1&page_size=100&jsvar=requestId_24959748'
            url = str1+item['Channel']+str2+item['ID']+str3
            page = urllib2.urlopen(url).read()
            jsonVal = json.loads(page.decode("gbk"))
        except:
            jsonVal = 'NULL'
            print "comment url error!"
        item['Comment'] = jsonVal
        try:
            item['Total'] = str(jsonVal["result"]["count"]["total"])
        except:
            item['Total'] = 'NULL'
        try:
            title = response.xpath("id('artibodyTitle')/text()").extract()
            item['Title'] = title[0]
        except:
            title = response.xpath("//title/text()").extract()
            item['Title'] = title[0]
            artical = response.xpath("/html/body//p").extract()
            item['Artical'] = "".join(artical)
            return item
 
        artical = response.xpath("id('artibody')//p/text()").extract()
        item['Artical'] = "".join(artical)
        return item
