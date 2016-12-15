import textwrap

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!\n')

class ReverseHandler(tornado.web.RequestHandler):
	def get(self, inputs):
		self.write( inputs[::-1])

class WrapHandler(tornado.web.RequestHandler):
	def post(self):
		text  = self.get_argument('text')
		width = self.get_argument('width', 40)
		self.write(textwrap.fill(text, int(width)))

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
    	handlers=[
    		#(r"/reverse/(\W+)", ReverseHandler),
    		#(r"/wrap/", WrapHandler),
    		(r"/", IndexHandler)
    	]
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
