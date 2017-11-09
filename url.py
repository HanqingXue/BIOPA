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

url = [
    (r'/', IndexHandler),
    (r'/about', AboutHandler),
    (r'/vesion', VisionHandler),
    (r'/data', DataHandler),
    (r'/search', SearchHandler),
] 