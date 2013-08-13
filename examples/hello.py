#!/usr/bin/env python
# -*- coding: utf-8 -*-

from py3web import route, run

@route('/')
def root():
    return '<h1>Welcome </h1>'

@route('/hello/<name>')
def hello(name):
    return '<h1>Hello %s!</h1>' % name.title()

run(host='localhost', port=8080)