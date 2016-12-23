import os.path
import random

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index2.htm')
        #self.render('vesion.htm')

class VisionHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('vesion.htm')
        pass

class HeatMapHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('net.html')
        pass
class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('search.html')
        pass

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler), 
                  (r'/vesion', VisionHandler),
                  (r'/net', HeatMapHandler),
                  (r'/search', SearchHandler)],

        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()