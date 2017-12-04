#coding=utf-8

import tornado.web

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('test2.html', title = "Hello world")