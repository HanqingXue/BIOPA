import json

class mergeJSON(object):
	"""docstring for mergeJSON"""
	def __init__(self, firstJSON, secondJSON, outputName):
		super(mergeJSON, self).__init__()
		self.firstJSON  = firstJSON
		self.secondJSON = secondJSON
		self.outputName = outputName
		self.filePath   = '../files/'
		self.merge()

	def merge(self):
		out = open('{}.json'.format(self.outputName), 'w')
		#print self.filePath + self.firstJSON
		mergeDict = {}
		firstDict = {}

		firstJSONFile  = json.load( open(self.filePath + self.firstJSON) )
		secondJSONFile = json.load( open(self.filePath + self.secondJSON) )

		'''
		Map the gse data to dict object in orde to pack the data easily
		The dictionary "mergeDict" is used as struct to store the merge
		info from two dict.
		'''

		for gene in firstJSONFile:
			gse  = gene
			gene =  gene['Gene name']
			firstDict[gene] = gse
			mergeDict[gene] = {}


		print len(mergeDict)
		'''
		For dict mergeDict :
			key: the gene name
			field:
			 	pathway :The dict type store pathway data
			 	gse     :The dict type store gse     data 
		'''
		for key in mergeDict.keys():
			mergeDict[key]['pathway'] = secondJSONFile[key]
			mergeDict[key]['gse'] = firstDict[key]

		'''
		Package data together
		'''
		json.dump(mergeDict, out)

class mergeDrugData(object):
	"""docstring for mergeDrugData"""
	def __init__(self):
		super(mergeDrugData, self).__init__()
		self.path  = '../files/'
		self.run()
	
	def run(self):
		'''
		originJSON : the data json file include the gse and pathway info
		drugJSOn   : the data about the drug info
		'''
		originJSON = json.load( open('data.json') )
		drugJSON   = json.load( open(self.path+'drug.json'))
		'''
		Add the drug as the atrt of originJSON files
		indedx of originJSON is gene name
		'''

		for item in originJSON:
			originJSON[item]['drug'] = drugJSON[item]
		'''
		New a json to pachage info 
		'''
		newJSON = open('newData.json', 'w')
		json.dump(originJSON, newJSON)
		
if __name__ == "__main__":
	#mergeJSON('GSE.json', 'pathway.json', 'data')
	drug = mergeDrugData()