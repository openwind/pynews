#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Genial Wang'

from flask import Flask, request
import logging; logging.basicConfig(level=logging.INFO)
import sys, os,re
import json
from jinja2 import Environment, FileSystemLoader
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

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

def get_dict(path, num=5):
    argument = dict()
    index_list = []
    for i in range(1, num+1):
        value_list = []
        file_name = os.path.join(path, str(i)+".json")
        try:
            with open(file_name, "r") as f:
                load_dict = json.load(f)
            value_list.append(load_dict['Title'])
            value_list.append(load_dict['URL'])
            value_list.append(load_dict['Artical'].strip()[5:400])
        except:
            continue
        index_list.append(value_list)
    argument["files"] = index_list

    return argument

@app.route('/', methods=['GET', 'POST'])
def home():
    env = init_jinja2()
    html = env.get_template('index.html').render().encode('utf-8')
    return html

@app.route('/signin', methods=['GET'])
def signin_form():
    pass

@app.route('/news', methods=['POST'])
def signin():
    env = init_jinja2()
    arg = get_dict("../spider/data/sina/interest_news/", 20)
    html = env.get_template('news.html').render(arg).encode('utf-8')
    return html
    
if __name__ == '__main__':
    app.run()
    #print get_dict("../spider/data/sina/interest_news/", 20)

