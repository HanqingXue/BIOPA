import tornado.web
import tornado.log
import json
'''
Change the workspace to root path.
'''
import sys
sys.path.append('../')

from methods.dbutil import *
from methods.versionutil import *

class VisionHandler(tornado.web.RequestHandler):
    def post(self):
        noun1 = self.get_argument('noun1')
        db = DataBase()
        print db.get_database('BioPA').name

        result = db.search_item({'Entity1': noun1})

        versionData = []

        nodes = []
        edge_types = []
        for item in result:
            nodes.append(item['Entity1'])
            nodes.append(item['Entity2'])
            edge_types.append(item['Interaction'])
            versionData.append(set_edge(item['Entity1'], item['Entity2'], item['Interaction']))
        
        nodes = set(nodes)
        nodes = list(nodes)

        for node in nodes:
            versionData.append(set_node(node))

        color = ['#1139AA', '#1DC600', '#8840A7', '#20C3C9', '#C8AA64', '#4B2E32']
        edge2list = list(set(edge_types))
        edge_info = dict(zip(edge2list, color[:len(edge2list)]))
        #list(set(edge_types))
        self.render('vesion.html', hello= json.dumps(versionData), edge_types = edge_info)