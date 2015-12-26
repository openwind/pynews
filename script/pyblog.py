#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Genial Wang'

import logging; logging.basicConfig(level=logging.INFO)
import sys, os,re
from jinja2 import Environment, FileSystemLoader
reload(sys)
sys.setdefaultencoding('utf-8')

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
        path = ('../templates')
    env = Environment(loader=FileSystemLoader(path), **options)
    return env

def findtoc(html):
    r1 = re.compile(r'<h2.*?>(.*?)<\/h2>')
    m = re.findall(r1, html)
    return m

def get_file(path='../html/'):
    list_files = os.listdir(path)
    dirname = [x for x in list_files if os.path.isdir(path+x)]
    files = []
    for dir in dirname:
        temp_files = os.listdir(path+dir)
        dir_files = list(filter(lambda x: x.endswith('.html'),temp_files))
        if dir_files:
            dir_files = map(lambda x: os.path.splitext(x)[0],dir_files)
            dir_files.insert(0,dir)
            files.append(dir_files)
    return files

def render_template(template_name, args):
    env = init_jinja2()
    html = env.get_template(template_name+'.html').render(**args).encode('utf-8')
    try:
        if 'index' == template_name or 'aboutme' == template_name:
            _pwd = '../'+template_name+'.html'
        else:
            _pwd = os.path.join('../html', args['categories'], args['basename'])
        _dir = os.path.dirname(_pwd)
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        f = open(_pwd, 'w')
        f.write(html)
        logging.info("write at "+_pwd)
    except:
        logging.error('html dir not found')

def generate_meta(args):
    p = u'<meta name = "description" content="' + args['title']  + '">'
    p += u'<meta name = "Keywords" content="' + args['tags'] + '">'
    return p

def parse_md(md_pwd, mdp):
    dirname, filename = os.path.split(md_pwd)
    basename = os.path.splitext(filename)[0]+".html"
    categories = dirname.split("/")[-1]
    try:
        md = open(md_pwd,'r').read()
        utils = open('../templates/utils.html', 'r').read()
    except:
        logging.error('invalid md_pwd')
        return
    mdp.renderer.reset_toc()
    args, md = meta.parse(md)
    md = Environment().from_string(utils+md).render()
    content = mdp(md)
    item_toc = findtoc(content)
    args['categories'] = categories
    args['basename'] = basename
    args['content'] = content
    args['meta'] = generate_meta(args)
    args['item_toc'] = item_toc
    render_template('blog', args)
    return basename, args['title']


if __name__ == '__main__':
    renderer = TocRenderer(linenos=True, inlinestyles=False)
    mdp = mistune.Markdown(escape=True, renderer=renderer)
    parse_md_all(mdp)
