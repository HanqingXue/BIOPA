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

class DrugHandler(tornado.web.RequestHandler):
	def initialize(self, db_session):
		self.entity_mapper = EntityMapper(db_session)

	@tornado.web.asynchronous
	def get(self):
		keyword =self.get_argument("keyword", None)
		geneinfo = self.entity_mapper.get_selected_gene_ids(keyword)
		drugs = self.entity_mapper.get_selected_relate_drug(geneinfo['entrez'])
		diseases = self.entity_mapper.get_seleted_relate_omim_hgmd(keyword)
		data = {'status':0,'message':'successfully','data':[drugs, diseases]}
		self.finish(json.dumps(data))


class GenePathwayHandler(tornado.web.RequestHandler):
	def initialize(self, db_session):
		self.entity_mapper = EntityMapper(db_session)

	@tornado.web.asynchronous
	def get(self):
		keyword =self.get_argument("keyword", None)
		geneinfo = self.entity_mapper.get_selected_gene_ids(keyword)
		super_pathway = self.entity_mapper.get_seleted_relate_superpathway(keyword)
		summary = self.entity_mapper.get_selected_gene_summary(geneinfo['entrez'])
		ensembl_id = self.entity_mapper.get_selected_gene_ensembl_id(geneinfo['entrez'])
		pubmed_id = self.entity_mapper.get_seleted_relate_pubmedids(geneinfo['entrez'])
		data = {'status':0,'message':'successfully','data':[geneinfo, summary, ensembl_id, pubmed_id, super_pathway]}
		self.finish(json.dumps(data))