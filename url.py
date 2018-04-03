#coding=utf-8
'''
the url structure of website
'''

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

url = [
    (r'/', IndexHandler),
    (r'/about', AboutHandler),
    (r'/vesion', VisionHandler),
    (r'/data', DataHandler),
    (r'/contact', ContactHandler),
    (r'/search', SearchHandler),
    (r'/test', TestHandler),
    (r'/pathway', PathwayHandler),
    (r'/pathwayplot', PlotHandler),
] 