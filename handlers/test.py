#coding=utf-8

import tornado.web

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('test.html', title = "Hello world")