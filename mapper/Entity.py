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

class Ensemblinfo(Base):
	"""docstring for Ensemblinfo"""
	__tablename__ = "gene2ensembl_ensembl"
	table_ID = Column(Integer, primary_key=True)
	gene_id = Column(String(64))
	entrez_id = Column(Integer)
	Refseq_rna = Column(String(64))
	Refseq_protein = Column(String(64))
	Ensembl_gene = Column(String(64))
	Ensembl_rna = Column(String(64))
	Ensembl_protein = Column(String(64))
	Ensembl_description = Column(String(64))

class Uniprotinfo(object):
	"""docstring for """
	__tablename__ = "gene2uniprot_uniprot"
	table_ID = Column(Integer, primary_key=True)
	gene_id = Column(String(64))
	Uniprot_id = Column(String(64))
	PDB_id = Column(String(64))
	InterPro_id = Column(String(64))
	InterPro_name = Column(String(64))
	Uniprot_description = Column(String(1024))
		