import os.path
import random

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from db import *

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('search.html', title = "Hello world")

class VisionHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('vesion.html')
        pass

class HeatMapHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('net.html')
        pass

class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('search.html')
        pass

class AboutHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
        pass

class DataHandler(tornado.web.RequestHandler):
    '''
    def get(self):
        query = self.get_argument("query")
        print query
        self.render('data.html')
    '''

    def post(self):
        noun1 = self.get_argument('noun1')
        db = DataBase()
        print db.get_database('BioPA').name
        result = db.search_item({'PathID': noun1})
        if len(result) == 0:
            self.render('error.html')
        else:
            self.render('data.html', noun1=result )

class UserHandler(tornado.web.RequestHandler):
    def post(self):
        user_name = self.get_argument("username")
        user_email = self.get_argument("email")
        user_website = self.get_argument("website")
        user_language = self.get_argument("language")
        self.render("user.html",username=user_name,email=user_email,website=user_website,language=user_language)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler), 
                  (r'/vesion', VisionHandler),
                  (r'/net', HeatMapHandler),
                  (r'/search', SearchHandler),
                  (r'/data', DataHandler),
                  (r'/user', UserHandler),
                  (r'/about', AboutHandler)],

        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()



