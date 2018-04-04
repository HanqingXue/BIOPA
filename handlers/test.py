#coding=utf-8

import tornado.web
import sys
sys.path.append('../')

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('compound.html')