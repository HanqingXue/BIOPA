import tornado.web

class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('search.html')