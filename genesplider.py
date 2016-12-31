#coding=utf-8
import re 
import sys
import os
from bs4 import BeautifulSoup
import requests
from lxml import etree
import json

reload(sys)

class geneSplider(object):
	"""docstring for geneSplider"""
	def __init__(self, gene):
		super(geneSplider, self).__init__()
		self.gene = gene
		self.baseurl = "http://cancer.sanger.ac.uk/cosmic/gene/analysis?ln="

	def run(self):
		self.url = self.baseurl + self.gene
		self.content = requests.get(self.url).content
		genePrase    = BeautifulSoup(self.content, 'lxml').findAll('div', class_="scrollable")
		print len(genePrase)
		for gene in genePrase:
			if len(gene.findAll('dl')) != 0:
				overView = gene.findAll('dl')
				for elm in overView:
					dts =  elm.findAll('dt')
					dds =  elm.findAll('dd')
					field = [text.text for text in dts if len(text.text) != 0 ]
					value = [text.text for text in dds if len(text.text) != 0 ]
					self.info = dict(zip(field, value))
					output = open('gene.json', 'w')
					json.dump( self.info, output)
			else:
				continue



if __name__ == "__main__":
	splider = geneSplider('TP53')
	splider.run()
	print splider.info