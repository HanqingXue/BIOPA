#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from Entity import *
from methods.WebParseHelper import *
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
			logging.error('Error occurred: %s in querying gene ids' % ex)
		return gene_info


	def get_selected_gene_summary(self, entrez_id):
		summary_info = ''
		
		try:
			result_proxy = self.db_session.execute('SELECT * FROM gene_summary_ncbi where entrez_id = :entrez_id;', {
				'entrez_id': entrez_id
			}).fetchall()

			if len(result_proxy) == 0:
			 	summary_info = ''
			else:
				summary_info = result_proxy[0][1]
		except Exception as ex:
			logging.error('Error occurred %s in querying gene summary'  % ex)
			summary_info = '' 

		return summary_info

	def get_selected_gene_ensembl_id(self, entrez_id):
		ensembl_id = ''

		try:
			ensembl_info = self.db_session.query(Ensemblinfo).filter(Ensemblinfo.entrez_id == entrez_id).first()
			ensembl_id = ensembl_info.gene_id
		except Exception as ex:
			logging.error('Error occurred %s in querying ensembl_id' % ex)

		return ensembl_id

	def get_selected_gene_uniport(self, ensembl_id):
		uniprot_id = ''

		try:
			uniprot = self.db_session.query(Uniprotinfo).filter(Uniprotinfo.gene_id == ensembl_id).one()
			uniprot_id = uniport.Uniprot_id
		except Exception as ex:
			logging.error('Error occurred %s in qrurying uniport ' % ex)

		return uniprot_id

	def get_selected_relate_drug(self, entrez_id):
		result_proxy = {}
		try:
			result = self.db_session.execute('SELECT * FROM drugtarge_pharmagkbttd where entrez_id = :entrez_id;', {
				'entrez_id': entrez_id
			}).fetchall()

			for item in result:
				if item[1] not in result_proxy.keys():
					result_proxy[item[1]] = item[-1]
				else:
					continue

		except Exception as ex:
			logging.error('Error occurred %s in qrurying drug' % ex)

		return result_proxy
	
	def get_selected_relate_drug_id(self, entrez_id):
		result_proxy = {}
		try:
			result = self.db_session.execute('SELECT * FROM drugtarge_pharmagkbttd where entrez_id = :entrez_id;', {
				'entrez_id': entrez_id
			}).fetchall()

			for item in result:
				if item[0] not in result_proxy.keys():
					result_proxy[item[0]] = item[-1]
				else:
					continue
		except Exception as ex:
			logging.error('Error occurred %s in qrurying drug' % ex)

		return result_proxy


	def get_selected_relate_disease(self, drugbank_id):
		result_proxy = {}
		try:
			result_proxy = self.db_session.execute('SELECT drug_commonname, indication, sources FROM drugtodisease_all WHERE drugtodisease_all.DrugBank_id = :drugbank_id;', {'drugbank_id': drugbank_id}).fetchall()
		except Exception as e:
			raise e
		
		return result_proxy 

	def get_seleted_relate_all_diseases(self, drug_ids):
		diseases = []
		result_proxy = {}

		for drug in drug_ids:
			diseases.extend(self.get_selected_relate_disease(drug))

		for index in range(0, len(diseases)):
			disease = {}
			disease['name'] = diseases[index][1]
			disease['drug'] = diseases[index][0]
			disease['source'] = diseases[index][-1]
			result_proxy[index] = disease

		return result_proxy

	def get_seleted_relate_pubmedids(self, entrez_id):
		pubmedids = ''
		try:
			result_proxy = self.db_session.execute('SELECT pubmed_id FROM gene_pumedid_ncbi where entrez_id = :entrez_id;', {'entrez_id': entrez_id}).fetchone()
			
			if result_proxy == None:
				result_proxy = ''
			else:
				result_proxy = result_proxy[0]

		except Exception as e:
			raise e

		return result_proxy

	def get_seleted_relate_superpathway(self, gene_symbol):
		result_proxy = {}
		try:
			result_proxy = pathcards_parser(gene_symbol)
			
		except Exception as ex:
			logging.error('Error occurred %s in querying pathway' % ex)
		
		return result_proxy

	def get_seleted_relate_omim_hgmd(self, gene_symbol):
		result_hgmd = self.db_session.execute( 'SELECT dbSNP_ID, disease_name FROM variation_hgmd where gene_symbol = :gene_symbol;', {'gene_symbol': gene_symbol}).fetchall()
		result_omim = self.db_session.execute( 'SELECT omim_id, Phenotype_Combind FROM variation_omim WHERE gene_symbol = :gene_symbol;', {'gene_symbol': gene_symbol}).fetchall()
		key = 0
		result_proxy = {}

		for row in result_hgmd:
			if row[1] in result_proxy.keys():
				result_proxy[row[1]] = 'dbSNP'
			else:
				result_proxy[row[1]] = {}
				result_proxy[row[1]] = 'dbSNP' 


		for row in result_omim:
			if row[1] == 'null':
				continue

			if row[1] in result_proxy.keys():
				result_proxy[row[1]] = 'OMIM'
			else:
				result_proxy[row[1]] = {}
				result_proxy[row[1]] = 'OMIM'

		return result_proxy

	def get_net(self, gene_symbol):
		result_proxy = self.db_session.execute("SELECT * from pathwaycommons9allhgnc WHERE (A2M = :gene_symbol or A1BG= :gene_symbol) and `controls-expression-of` != :edge", {'gene_symbol': gene_symbol, 'edge' : "chemical-affects"}).fetchall()
		version_data = []

		if len(result_proxy) == 0:
			return version_data

		for row in result_proxy:
			pathway = {}
			pathway['Entity1'] = row[1]
			pathway['Entity2'] = row[3]
			pathway['Interaction'] = row[2]
			pathway['PathID'] = 'ipa'
			pathway['PathName'] = 'ipa'
			pathway['ManuscriptID'] = '21900206;|imex:IM-16799'
			version_data.append(pathway)

		return version_data