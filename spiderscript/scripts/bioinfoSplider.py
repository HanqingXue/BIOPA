#coding=utf-8
import re 
import sys
import os
from bs4 import BeautifulSoup
import requests
from lxml import etree
import json
import traceback 

reload(sys)

class geneSplider(object):
	"""docstring for geneSplider"""
	def __init__(self, gene):
		super(geneSplider, self).__init__()
		self.gene = gene
		self.baseurl = "http://cancer.sanger.ac.uk/cosmic/gene/analysis?ln="

	def run(self):
		'''Run a instance of genespider
		Get the url of cosmic database and exact the data of overview page
		
		Args: Object self

		Return : a JSON object which have multifiled.
			example: 
				for gene TP53 in cosmic darabase the overview can be
			listed as blow format
			{
			    "Pfam": " P04637",
			    "Alternative Transcripts": "TP53_ENST00000545858, TP53_ENST00000269305, TP53_ENST00000455263, TP53_ENST00000414315, TP53_ENST00000413465, TP53_ENST00000420246 ",
			    "Atlas Genetic Oncology": "P53ID88",
			    "Transcript": "ENST00000269305",
			    "CCDS": "CCDS11118.1",
			    "OMIM": "191170",
			    "TP53 is involved in fusions with :": "\nNTRK1_ENST00000392302 ( 1 mutations in 38 samples )  \n                  ",
			    "Genomic Coordinates": "\n17:7669609..7676594 \n          (negative strand)\n        ",
			    "Synonyms": "LFS1,P53,TRP53,p53,CCDS11118.1,P04637,ENSG00000141510",
			    "IARC": "IARC TP53 Database",
			    "Copy Number": "CONAN",
			    "Gene name": "TP53\n        \n This is a known cancer gene, for more information please look here\n\n This is an expert curated gene, for more information please look here\n",
			    "No.of Samples": "\n          Total number of unique samples: 125062 \n          Unique samples with mutations:  30504\n          ",
			    "Drug Sensitivity Data:": "Mutations in TP53 are associated with altered sensitivity to the following drug(s) :  Imatinib more\n\nAZD-0530,  GNF-2,  Epothilone B,  AICAR,  Docetaxel,  Methotrexate,  CCT018159,  Nutlin-3a,  Etoposide,  GNF-2,  Epothilone B,  Thapsigargin,  OSU-03012,  Nutlin-3a\nClick here for all TP53 drug sensitivity data\n         \n",
			    "Protein Sequence": "TP53",
			    "Gene Id": "COSG501",
			    "Transcript and Protein Aligned": "ENST00000269305+TP53",
			    "Swiss-prot": "P04637",
			    "cDNA Sequence": "ENST00000269305",
			    "Genome Browsers": "Ensembl, UCSC",
			    "HGNC": "11998"
			}
		'''
		self.url = self.baseurl + self.gene
		self.content = requests.get(self.url).content
		genePrase    = BeautifulSoup(self.content, 'lxml').findAll('div', class_="scrollable")
		'''
		Splider fail or dont have this gene detail
		'''


		if len(genePrase) == 0:
			log = open('log.txt', 'a')
			log.write(self.gene+'\n')
			log.close()
			return 0
		'''
		Splider catches information
		'''
		
		for gene in genePrase:
			if len(gene.findAll('dl')) != 0:
				overView = gene.findAll('dl')
				for elm in overView:
					#The dt label store the table haed of overvirwinfo
					dts =  elm.findAll('dt')
					#The dd labek store the content in deatil of ovrerview
					dds =  elm.findAll('dd')
					#fields store keys of overview ,infomations were exacted 
					#from dt label 
					fields = [text.text for text in dts if len(text.text) != 0 ]
					#values store the value of overview, information were exacted
					#from dd label
					values = [text.text for text in dds if len(text.text) != 0 ]
					#map the keys and values
					self.info = dict(zip(fields, values))
					self.info['Gene name'] = self.gene
					#output = open('gene.json', 'w')
					#json.dump( self.info, output)
	
			else:
				continue

		return 1

class KEGGSplider(object):
	"""docstring for KEGGSplider"""
	'''
	Init function of KEGG splider
	Args: 
		gene: string type that stand for the name of gene
		self: Object self 
	'''
	def __init__(self, gene):
		super(KEGGSplider, self).__init__()
		self.gene    = gene
		self.baseurl = "http://www.genome.jp/dbget-bin/www_bfind_sub?mode=bfind&max_hit=1000&dbkey=genes&keywords="
		self.pathway      = {}

	'''
	Run a instance of kegg splider, get the Url of kegg database to 
	exact the relanvace pathway
	Args:
		Object self
	Return:
	    A dict object
	example: for gene TP53 
		the key of return dict is 'TP53'
		the value of return dict is a dictionary object
		:
			key  : the id of pathway
			value: the discript of this pathway
	'''

	def run(self):
		'''
		Baseurl is an url which use kegg database gene search;
		Self.content include the all of content on the page
		'''
		self.url     = self.baseurl + self.gene
		self.content = requests.get(self.url).content
		'''
		paPrase is praser of page
		'''
		paPrase      = BeautifulSoup(self.content, 'lxml').form    #.find('form')
		'''
		The discript of div label can be divided into two class, we 
		can use stylesheet to label them :
			margin-left:2em ------- discription of PA
			width:600px     ------- include the link of PA id
		'''
		pathwayDict = {}
		keys = []
		values = []
		for pa in  paPrase.find_all('div'):
			if pa['style'] == 'margin-left:2em':
				values.append(pa.text)
			elif pa['style'] == 'width:600px':
				keys.append(pa.a.text)
			else:
				pass
		#pathwayDict = dict(zip(keys, values))
		self.pathway[self.gene] = dict(zip(keys, values))
		#print self.pathway
		return 1

class drugSplider(object):
	"""docstring for drugSplider"""
	'''
	Init the drugSplider
	Args: 
	gene: string type that stand for the name of gene
	self: Object self 
	'''
	def __init__(self, gene):
		self.gene = gene
		self.url = "http://www.kegg.jp/kegg-bin/search?q={}&display=disease&uid=148337620745467&from=drug&target=compound%2bdrug%2bdgroup%2benviron%2bdisease" .format(self.gene)
		self.info = {}
		self.run()

	'''
	Run a instance of drug splider, get the Url of kegg database to 
	exact rugs and diseases
	Args:
		Object self
	Return:
	    A dict object
	example: for gene TP53 
		For return dicr object:
		Key:   the disease code such as H000004
		Value: Name, Description,	Category,  PathwayDrug
	'''
	def run(self):
		print self.url
		self.content = requests.get(self.url).content
		drugs = BeautifulSoup(self.content, 'lxml').findAll('table', class_="list1")
		'''
		The fields meanings one row in a table,the index of fields
		defined blow:
		Index:
		0 Entry      : the id of disease
		1 Name       : the name of disease
		2 Description: the discription of disease
		3 Category   : the category of disese
		4 pathway    : the pathway infomation
		5 Drug       : the drug info

		'''
		self.info[self.gene] = {}
		for row in drugs[0].findAll('tr'):#get the row

			fields = row.findAll('td')
			if len(fields) == 6:
				Entry         = fields[0].text.strip('\n')
				Name          = fields[1].text.strip('\n')
				Description	  = fields[2].text.strip('\n')
				Category	  = fields[3].text.strip('\n')
				Pathway	      = fields[4].text.strip('\n')
				Drug	      = fields[5].text.strip('\n')

				'''
				Define the return dict object of splider, this nested 
				dict object
				For out layer:
					key: the Entry 
					value: a dict which include the Name, Description, Category
					, pathway, Drug
				For in layer:
					key:  Name, Description, Category, pathway, Drug
					value: the detail info about this field which exact from origin table
				'''
				self.info[self.gene][Entry] = {}#out layer
				self.info[self.gene][Entry]['Name']        = Name#in layer
				self.info[self.gene][Entry]['Description'] = Description#in layer
				self.info[self.gene][Entry]['Category']    = Category #in layer
				self.info[self.gene][Entry]['Pathway']     = Pathway#in layer
				self.info[self.gene][Entry]['Drug']        = Drug#in layer

			else:
				continue
		return 1

class main(object):
	"""Exact multigene overview information from network and store in the Json files"""
	'''
	Init the main function
	Args: 
		JSONname: a string that is output file's name
		geneFile: a string that store all of gene name for splider
	Return:
		A JSON file that store all of the gene's detail info.
	'''
	def __init__(self, JSONname, geneFile):
		super(main, self).__init__()
		self.JSONname = JSONname
		self.genesName = geneFile
		self.run()
			
	def run(self):
		print 'Splider working'
		infoList = {}
		jsonaFile = open(self.JSONname, 'w')
		genes = open(self.genesName)
		genes = [item[0:-1] for item in genes.readlines()]
		
		try:
			for gene in genes:
				print gene
				splider = drugSplider(gene)
				#print splider
				if splider.run() == 1:
					print 'ok'
					infoList[gene] = splider.info[gene]
					#infoList.append(splider.pathway)
				else:
					continue
			json.dump(infoList, jsonaFile)
			print "Splider work done"
		except :
			traceback.print_exc()



if __name__ == "__main__":
	main('../files/drug.json', '../files/gene.txt')
	#main()
	pass

