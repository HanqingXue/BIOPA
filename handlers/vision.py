#coding=utf-8

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
from methods.simulation import *

class VisionHandler(tornado.web.RequestHandler):
    def initialize(self, db_session):
        self.db_session = db_session

    def post(self):
        noun1 = self.get_argument('noun1')
        '''
        db = DataBase()
        print db.get_database('BioPA').name

        result = search_db(db, 'BioPA', 'Entity1', noun1)
        '''

        result = simulation()

        versionData = []

        nodes = []
        edge_types = []
        for item in result:
            nodes.append(check_node_Id(item['Entity1']))
            nodes.append(check_node_Id(item['Entity2']))
            edge_types.append(item['Interaction'])
            versionData.append(
                set_edge_test(check_node_Id(item['Entity1']), 
                check_node_Id(item['Entity2']), 
                item['Interaction'], 
                item['PathID'], 
                item['PathName'], 
                item['ManuscriptID']))

        nodes = set(nodes)
        nodes = list(nodes)

        for node in nodes:
            versionData.append(set_node(node))

        edge2list = list(set(edge_types))
        edge_info = {
            'CAI': '#8840A7',
            'BRR': '#1139AA',#1139AA
            #'MI': '#1DC600',
            'MI': '#ADADAD',
            'TBRR': '#20C3C9',
            'ER': '#C8AA64',
            'OTHER': '#4B2E32',
            'CAR': '#FFFFFF'
        }
        #print versionData
        self.render('vesion.html', hello= json.dumps(versionData), edge_types = dict([(key, edge_info[key]) for key in edge2list]))

    def get(self):
        str1 =self.get_argument("dat",None)
        print str1
        data = {'status':0,'message':'successfully','data':[str1]}
        self.write(json.dumps(data))