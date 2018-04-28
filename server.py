#coding=utf-8

import tornado.ioloop
import tornado.options
import tornado.httpserver

from application import application
from tornado.options import define, options

define("host", default ='127.0.0.1', help = "The url of the application", type = str)
define("port", default = 8000, help = "", type = int)

def main():
	tornado.options.parse_command_line()
	httpserver = tornado.httpserver.HTTPServer(application)
	httpserver.listen(options.port)

	print 'Developmet sever is runnint at http://{0}:{1}'.format(options.host, options.port)
	print 'Quit the sever with Ctrl-C'

	tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
	main()