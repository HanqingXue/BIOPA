import tornado.web
'''
Change the workspace to root path.
'''
import sys
sys.path.append('../')

from methods.dbutil import *

class PathwayHandler(tornado.web.RequestHandler):
    def post(self):
    	'''
    	Get arguments from front page. 
    	'''
        noun1 = self.get_argument('noun1')
        self.render("pathviz.html")