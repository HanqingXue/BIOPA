import tornado.web
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
        result = db.search_item({'PathID': noun1})

        versionData = []
        nodes = []
        for item in result:
            nodes.append(item['Entity1'])
            nodes.append(item['Entity2'])
            versionData.append(set_edge(item['Entity1'], item['Entity2']))
        nodes = set(nodes)
        nodes = list(nodes)

        for node in nodes:
            versionData.append(set_node(node))

        self.render('vesion.html', hello= json.dumps(versionData))