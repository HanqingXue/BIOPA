#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import tornado.web
import os
from handlers.about import AboutHandler
from handlers.vision import VisionHandler
from handlers.search import SearchHandler
from handlers.contact import ContactHandler
from handlers.test import DrugHandler
from handlers.test import GenePathwayHandler
from handlers.test import SearchNetHandler
from handlers.test import KEGGSearchHandler
from handlers.test import PathvizHandler
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.httpserver import HTTPServer
from tornado.options import define, options
from tornado.ioloop import IOLoop
import config

from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from mapper.EntityMapper import *

define("http_port", default = 8000, help = "run on the given port", type = int)

class Application(tornado.web.Application):
	def __init__(self, base_url, db_session):
		"""The constructor of Tornado Application.
		Args:
			self: the Application itself.
			db_session: The connection of MySQL
		"""
		handlers = [
			(r'/about', AboutHandler),
			(r'/', VisionHandler, dict(db_session=db_session)),
			(r'/contact', ContactHandler),
			(r'/search', SearchHandler),
			(r'/test', DrugHandler, dict(db_session=db_session)),
			(r'/gene', GenePathwayHandler, dict(db_session=db_session)),
			(r'/searchnet', SearchNetHandler, dict(db_session=db_session)),
			(r'/kegg', KEGGSearchHandler),
			('/pathviz', PathvizHandler)
		] 

		settings = dict(
			template_path = os.path.join(os.path.dirname(__file__), "templates"),
			static_path = os.path.join(os.path.dirname(__file__), "static"),
			debug = True
		)

		tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
	'''
	setUp MySQL connection
	'''
	db_engine = create_engine('mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}'.format(
		config.mysql_username, 
		config.mysql_password, 
		config.mysql_host, 
		config.mysql_port, 
		config.mysql_database))

	db_session  = scoped_session(sessionmaker(bind=db_engine,
						autocommit=True, autoflush=True, expire_on_commit=False))
	'''
	Start HTTP Server
	'''
	http_server = HTTPServer(Application(config.base_url, db_session), max_buffer_size=10485760000)
	http_server.listen(options.http_port)
	IOLoop.current().start()