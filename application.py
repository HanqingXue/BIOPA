#coding=utf-8

from url import url 
import tornado.web
import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from handlers.index import IndexHandler
from handlers.about import AboutHandler
from handlers.vision import VisionHandler
from handlers.data import DataHandler
from handlers.search import SearchHandler
from handlers.contact import ContactHandler
from handlers.test import TestHandler
from handlers.pathway import PathwayHandler
from handlers.plot import PlotHandler

settings = dict(
	template_path = os.path.join(os.path.dirname(__file__), "templates"),
	static_path = os.path.join(os.path.dirname(__file__), "static"),
	debug = True
	)

application = tornado.web.Application(
	handlers = url, 
	**settings
	)

class Application(tornado.web.Application):
	def __init__(self, base_url, db_session):
		"""The constructor of Tornado Application.
		Args:
			self: the Application itself.
			db_session: The connection of MySQL
		"""

		handlers = [
			(r'/', IndexHandler),
			(r'/about', AboutHandler),
			(r'/vesion', VisionHandler, dict(db_session=db_session)),
			(r'/data', DataHandler),
			(r'/contact', ContactHandler),
			(r'/search', SearchHandler),
			(r'/test', TestHandler),
			(r'/pathway', PathwayHandler),
			(r'/pathwayplot', PlotHandler),
		] 

		settings = dict(
			template_path = os.path.join(os.path.dirname(__file__), "templates"),
			static_path = os.path.join(os.path.dirname(__file__), "static"),
			debug = True
		)

		tornado.web.Application.__init__(self, handlers, **settings)