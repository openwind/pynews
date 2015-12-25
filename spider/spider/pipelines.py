# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import os
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SpiderPipeline(object):
    def __init__(self):
        global var_count
        global var_set
        global base_dir
        var_count = 1
        base_dir = "data/"

    def process_item(self, item, spider):
        global var_count
        global base_dir

        dir_name1 = base_dir+item['Source']+'/interest_news/'
        file_name = str(var_count)+'.json'
        if not os.path.exists(dir_name1):
            os.makedirs(dir_name1)
        file1 = codecs.open(os.path.join(dir_name1, file_name), mode='wb',encoding='utf-8')
        d = dict(item)
        del d['Comment']
        del d['Html']
        line = json.dumps(d,sort_keys=True,skipkeys=True,indent=4)
        file1.write(line.decode("unicode_escape"))

        dir_name2 = base_dir+item['Source']+'/comments/'
        if not os.path.exists(dir_name2):
            os.makedirs(dir_name2)
        file2 = codecs.open(os.path.join(dir_name2, file_name), mode='wb', encoding='utf-8')
        line = json.dumps(item['Comment'],indent=4)
        file2.write(line.decode("unicode_escape"))

        dir_name3 = base_dir+item['Source']+'/html/'
        if not os.path.exists(dir_name3):
            os.makedirs(dir_name3)
        file3 = codecs.open(os.path.join(dir_name3, file_name), mode='wb', encoding='utf-8')
        h = "".join(item['Html'])
        file3.write(h)

        print var_count,d['Title'].decode('utf-8'),d['Time']
        print "ID:",d['ID'],d['URL']
        print d['Artical'][0:40]
        #var_set.add(item['URL'])
        var_count += 1
        print spider.name
        return item
