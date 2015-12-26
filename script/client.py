#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Genial Wang'


def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return '<h1>Hello, web!</h1>'
