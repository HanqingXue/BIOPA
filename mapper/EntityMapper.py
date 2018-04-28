#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from Entity import *
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

class EntityMapper(object):
	"""docstring for EntityMapper"""
	def __init__(self, db_session):
		self.db_session = db_session

	def get_selected_gene_ids(self, gene_symbol):
		gene_info = {}

		try:
			gene = self.db_session.query(Geneinfo).filter(Geneinfo.Gene_Symbol == gene_symbol).one()	
			gene_info = {
				'entrez': gene.entrez_id,
				'HGNC': gene.HGNC_id,
				'synonyms': gene.synonyms,
				'chr':gene.Chr,
				'chromosome_band': gene.chromosome_band,
				'type':gene.type_of_gene,
				'description': gene.description
			}	
		except Exception as ex:
			logging.error('Error occurred: %s' % ex)
		return gene_info


	def get_selected_gene_summary(self, entrez_id):
		summary_info = ''
		
		try:
			summary = self.db_session.query(Summaryinfo).filter(Summaryinfo.entrez_id == 9997).one()
			summary_info = summary.Summary 
		except Exception as ex:
			logging.error('Error occurred %s' % ex)

		return summary_info