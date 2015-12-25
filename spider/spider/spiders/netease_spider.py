# -*- coding : utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as sle
from scrapy.selector import Selector
from spider.items import SpiderItem
import urllib2
import string
import json
import re

class NeteaseSpider(CrawlSpider):
    name = "neteasespider"
    allowed_domains = ["news.163.com"]
    start_urls = [
            "http://news.163.com/"
            #"http://news.163.com/15/1225/14/BBMHVKNA000156PO.html"
            ]
    rules = [
        Rule(sle(allow = ('[0-9,a-z,A-Z]\.html$',)), callback = 'parse_home', process_request = 'add_cookie'),
        Rule(sle(allow = ('/$',)), follow = True, process_request = 'add_cookie'),
        ]

    def add_cookie(self, request):
        request.replace(cookies = [
            {'name':'COOKIE_NAME', 'value':'VALUE', 'domain':'news.163.com', 'path':'/'},
            ])
        return request

    def parse_home(self, response):
        item = SpiderItem()
        url_info = response.url.split('/')

        item['Html'] = response.xpath("//html").extract()
        item['Source'] = 'netease'
        item['URL'] = response.url

        try:
            item['Time'] = "20"+url_info[3]+url_info[4]
        except:
            item['Time'] = "NULL"

        try:
            item['ID'] = url_info[6].split('.')[0]
            #item['Channel'] = url_info[3]
        except:
            item['ID'] = "NULL"
            #item['Channel'] = "NULL"
        #try:
        #    time = sel.xpath("//span[@id='pub_date']/text()").extract
        #    item['Time'] = time[0]
        #except:
        #    item['Time'] = 'NULL'
        try:
            words = response.xpath("//head/meta[@name='keywords']/@content").extract()
            item['Keyword'] = ",".join(words)
        except:
            item['Keyword'] = 'NULL'
        #try:
        #    str1 = "http://coral.qq.com/article/"
        #    str2 = "/comment?commentid=0&reqnum=20&tag=&callback=mainComment&_=1389623278900"
        #    url = str1+cmt_id+str2
        #    page = urllib2.urlopen(url).read()
        #    url_text = page[page.index("(")+1 : len(page)-1]
        #    jsonVal = json.loads(url_text.decode("utf-8"))
        #except:
        #    jsonVal = 'NULL'
        #    print "comment url error!"
        item['Comment'] = "NULL"
        try:
            item['Total'] = response.xpath("//script").re("totalCount.=.([0-9]*)")[0]
        except:
            item['Total'] = 'NULL'
        try:
            title = response.xpath("id('h1title')/text()").extract()
            item['Title'] = title[0]
        except:
            item['Title'] = response.xpath("//head/title/text()").extract()
        try:
            artical = response.xpath("/html/body//p").extract()
            item['Artical'] = "".join(artical)
        except:
            item['Artical'] = "NULL"
 
        return item
