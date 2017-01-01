#coding=utf-8
import json

class HandleJson(object):
	"""docstring for HandleJson"""
	def __init__(self, fileName):
		super(HandleJson, self).__init__()
		self.fileName = fileName

	def run(self):
		netfile = open(self.fileName)
		try:
			'''
			Read the json file from disk
			'''
			net = netfile.read()
			netParsed = json.loads(net)
			nodes = set()
			geneList = open('gene.txt', 'w')
			'''
			Label edges
			'''
			for elms in netParsed:
				'''
				Lable the edges
				'''
				if elms['group'] == 'edges':
					edgeType =  elms['data']['type']
					elms['classes'] = 1 if edgeType == 'controls-state-change-of' else 0
				else:
					nodeType = elms['data']['importance']
					elms['classes'] = nodeType
					geneid = elms['data']['id']
					geneList.write("{0}\n".format(geneid))
			'''
			save the new json 
			'''
			#labelNet = open('net_new.json', 'w')
			#json.dump(netParsed, labelNet)
		finally:
			netfile.close()
def  main():
	netHandle = HandleJson('net.json')
	netHandle.run()
	pass

if __name__ == "__main__":
	main()
	pass

