#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Geneinfo(Base):
	__tablename__ = "geneinfo_ncbihgnc"

	table_ID = Column(Integer, primary_key=True)
	gene_id = Column(String(64))
	entrez_id = Column(Integer)
	Gene_Symbol = Column(String(32))
	HGNC_id = Column(String(32))
	synonyms = Column(String(64))
	Chr =  Column(String(32))
	chromosome_band = Column(String(32))
	type_of_gene = Column(String(32))
	description = Column(String(128))

class Summaryinfo(Base):
	"""docstring for Diseaseinfo"""
	__tablename__ = "gene_summary_ncbi"
	entrez_id = Column(String(64), primary_key=True)
	Summary = Column(String(1024))




class EntityMapper(object):
	"""docstring for EntityMapper"""
	def __init__(self, db_session):
		super(EntityMapper, self).__init__()
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
'''
def test_handle():
	user_name = "lijie"
	passwd = "lijie_kb5"
	host = "111.198.139.95"
	port = "3306"
	database = "medicine_database"
	engine = create_engine('mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}'.format(
		user_name, passwd, host, port, database))

	db_session  = scoped_session(sessionmaker(bind=engine,
                        autocommit=True, autoflush=True, expire_on_commit=False))

	gene_info = {}

	try:
		gene = EntityMapper(db_session)
		#gene_info = gene.get_selected_gene_ids('A2M')
		summary_info = gene.get_selected_gene_summary(111)

		#$print gene_info
		print summary_info
	except Exception as ex:
		logging.error('Error occurred: %s' % ex)

	pass
	

if __name__ == '__main__':
	test_handle()
'''