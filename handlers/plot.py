import tornado.web

import sys
import json
sys.path.append('../')

from methods.dbutil import *
from methods.versionutil import *

class PlotHandler(tornado.web.RequestHandler):
    def get(self): 
    	pathname = 'Insulin receptor signalling cascade.txt'
        result = open(pathname)
        versionData = []

        nodes = set()

        for item in result:
        	item = item.split('\t')
        	nodes.add(item[0])
        	nodes.add(item[1])
        	versionData.append(set_base_edge(item[0], item[1]))

        for item in nodes:
        	versionData.append(set_node(item))

        self.render('plotter.html', hello= json.dumps(versionData), pathname=pathname)

