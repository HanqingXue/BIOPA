#coding=utf-8

import tornado.web
import sys
sys.path.append('../')

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
from mapper.EntityMapper import EntityMapper

class TestHandler(tornado.web.RequestHandler):
    def initialize(self, db_session):
        self.entity_mapper = EntityMapper(db_session)

    @tornado.web.asynchronous
    def get(self):
    	keyword =self.get_argument("keyword", None)
        geneinfo = self.entity_mapper.get_selected_gene_ids(keyword)
        drugs = self.entity_mapper.get_selected_relate_drug(geneinfo['entrez'])
        data = {'status':0,'message':'successfully','data':[drugs]}
        self.finish(json.dumps(data))