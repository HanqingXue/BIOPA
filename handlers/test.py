#coding=utf-8

import tornado.web
import sys
sys.path.append('../')

import tornado.web
import tornado.log
import json
import random
'''
Change the workspace to root path.
'''
import sys
sys.path.append('../')

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

class SearchNetHandler(tornado.web.RequestHandler):
	def initialize(self, db_session):
		self.entity_mapper = EntityMapper(db_session)

	@tornado.web.asynchronous
	def get(self):
		'''
		Gete network here

		'''
		keyword =self.get_argument("keyword", None)
		result = self.entity_mapper.get_net(keyword)
		#result = simulation('toy.csv')
		testData = {}
		testData["nodes"] = []
		testData["edges"] = []

		for item in result: 
			source = {}
			source["data"] = {}
			if ';' in item['Entity1']:
				continue

			if ';' in item['Entity2']:
				continue

			source["data"]["id"] = item['Entity1']
			source["data"]["position"] = {}
			source["data"]["position"]['x'] = random.randint(0, 800)
			source["data"]["position"]['y'] = random.randint(0, 800)
			
			target = {}
			target["data"] = {}
			target["data"]["id"] = item['Entity2']

			testData["nodes"].append(source)
			testData["nodes"].append(target)

			edge = {}
			edge["data"] = {}
			edge["data"]["id"] = item['Entity1'] + "2" + item['Entity2']
			edge["data"]["source"] =  item['Entity1']
			edge["data"]["target"] = item['Entity2']
			edge["data"]["type"] = item['Interaction']
			edge["data"]['Manuscripts'] = item['Manuscripts']
			edge["data"]['resource'] = item['resource']
			edge["data"]['PathName'] = item['PathName']
			testData["edges"].append(edge)

		data = {'status':0,'message':'successfully','data':[json.dumps(testData)]}
		self.finish(json.dumps(data))