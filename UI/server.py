#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Genial Wang'

import sys, os,re,urllib
sys.path.append("../")
from flask import Flask, request
import logging; logging.basicConfig(level=logging.INFO)
import json
from jinja2 import Environment, FileSystemLoader
from invert.similarity import *
from relevant.relatesearch import *

app = Flask(__name__)

ppath='../spider/data/sina/interest_news'
corpus=cutWord(getFiles(ppath))
que = ""
sequence = ""
def init_jinja2(**kw):
    options = dict(
            autoescape = kw.get('autoescape', False),
            block_start_string = kw.get('block_start_string', '{%'),
            block_end_string = kw.get('block_end_string', '%}'),
            variable_start_string = kw.get('variable_start_string', '{{'),
            variable_end_string = kw.get('variable_end_string', '}}'),
            auto_reload = kw.get('auto_reload', True)
            )
    path = kw.get('path', None)
    if path is None:
        path = ('./templates')
    env = Environment(loader=FileSystemLoader(path), **options)
    return env

def get_list(path):
    index_list = []
    for file_name in path:
        value_list = []
        try:
            with open(file_name, "r") as f:
                load_dict = json.load(f)
            value_list.append(load_dict['Title'])
            value_list.append(load_dict['URL'])
            value_list.append(load_dict['Artical'].strip()[5:400])
            if load_dict['Time'] == "":
                value_list.append("0")
            else:
                value_list.append(load_dict['Time'])
                print load_dict['Time'] + "  " + file_name
            if load_dict['Total'] == "":
                value_list.append("0")
            else:
                value_list.append(load_dict['Total'])
            print "Time:"+ load_dict['Time'] + "    Total:"+ load_dict['Total']
        except:
            continue
        index_list.append(value_list)
    return index_list

def handle(search, seq):
    arg = dict()
    env = init_jinja2()
    if search == "":
        html = env.get_template('index.html').render().encode('utf-8')
    else:
        degree=sortResult(query(search,corpus,ppath))
        filelist = [info[0] for info in degree]
        argList = get_list(filelist)
        if seq == "time":
            sortByTime(argList)
        elif seq == "hot":
            sortByHot(argList)
        arg['files'] = argList
        arg['search'] = search
        result_list = relate_search(search)
        arg['rel'] = result_list
        #渲染结果页面
        html = env.get_template('news.html').render(arg).encode('utf-8')
    return html

@app.route('/', methods=['GET', 'POST'])
def home():
    env = init_jinja2()
    html = env.get_template('index.html').render().encode('utf-8')
    return html

@app.route('/news', methods=['GET'])
def test():
    que = request.args.get('search')
    return handle(que, sequence)

@app.route('/news', methods=['GET', 'POST'])
def news():
    # 用这两个参数进行检索和排序
    que = request.form['search']
    try:
        sequence = request.form['radio']
    except:
        sequence = ""
    return handle(que, sequence)

if __name__ == '__main__':
    app.run()
    #print get_dict("../spider/data/sina/interest_news/", 20)
    #relative_compute(u"中华人民共和国")
