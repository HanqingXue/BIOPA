#coding=utf-8

import tornado.ioloop
import tornado.options
import tornado.httpserver

from application import application

from tornado.options import define, options

define("port", default = 8000, help = "run on the given port", type = int)

def main():
	tornado.options.parse_command_line()
	httpserver = tornado.httpserver.HTTPServer(application)
	httpserver.listen(options.port)

	print 'Developmet sever is runnint at http://127.0.0.1:{}'.format(options.port)
	print 'Quit the sever with Ctrl-C'

	tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
	main()