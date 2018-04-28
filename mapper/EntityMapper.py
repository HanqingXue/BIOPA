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
			summary = self.db_session.query(Summaryinfo).filter(Summaryinfo.entrez_id == entrez_id).one()
			summary_info = summary.Summary 
		except Exception as ex:
			logging.error('Error occurred %s' % ex)
			summary_info = '' 

		return summary_info

	def get_selected_gene_ensembl_id(self, entrez_id):
		ensembl_id = ''

		try:
			ensembl_info = self.db_session.query(Ensemblinfo).filter(Ensemblinfo.entrez_id == entrez_id).one()
			ensembl_id = ensembl_info.gene_id
		except Exception as ex:
			logging.error('Error occurred %s' % ex)

		return ensembl_id

	def get_selected_gene_uniport(self, ensembl_id):
		uniprot_id = ''

		try:
			uniprot = self.db_session.query(Uniprotinfo).filter(Uniprotinfo.gene_id == ensembl_id).one()
			uniprot_id = uniport.Uniprot_id
		except Exception as ex:
			logging.error('Error occurred %s' % ex)

		return uniprot_id
