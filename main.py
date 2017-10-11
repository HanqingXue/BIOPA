import os.path
import random
import json
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from dbutil import *
from versionutil import *
from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('search.html', title = "Hello world")

class VisionHandler(tornado.web.RequestHandler):
    def post(self):
        noun1 = self.get_argument('noun1')
        db = DataBase()
        print db.get_database('BioPA').name
        result = db.search_item({'PathID': noun1})

        versionData = []
        nodes = []
        for item in result:
            nodes.append(item['Entity1'])
            nodes.append(item['Entity2'])
            versionData.append(set_edge(item['Entity1'], item['Entity2']))
        nodes = set(nodes)
        nodes = list(nodes)

        for node in nodes:
            versionData.append(set_node(node))

        self.render('vesion.html', hello= json.dumps(versionData))

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
    def post(self):
        noun1 = self.get_argument('noun1')
        db = DataBase()
        print db.get_database('BioPA').name
        result = db.search_item({'PathID': noun1})
        if len(result) == 0:
            self.render('error.html')
        else:
            self.render('data.html', noun1=result, keyword=noun1 )


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler), 
                  (r'/vesion', VisionHandler),
                  (r'/net', HeatMapHandler),
                  (r'/search', SearchHandler),
                  (r'/data', DataHandler),
                  (r'/about', AboutHandler)],

        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()



