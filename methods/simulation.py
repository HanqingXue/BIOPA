#coding=utf-8
import csv
import random 

def simulation(name='network_bak.csv'):
	with open(name) as net:
		reader = csv.DictReader(net)
		version_data = []

		edge_type = \
			["interacts-with",
			"controls-phosphorylation-of",
			"controls-state-change-of"]

		
		for row in reader:
			pathway = {}
			source_entity = row['ID1']
			target_entity = row['ID2']
			index = random.randint(0,  len(edge_type))
			index = index - 1
			interaction = edge_type[index]
			pathway['Entity1'] = source_entity
			pathway['Entity2'] = target_entity
			pathway['Interaction'] = interaction
			pathway['Source'] = 'BioGRID'
			pathway['PathName'] = 'Transcriptional regulation of pluripotent stem cells'
			pathway['ManuscriptID'] = '21900206;23667531'
			version_data.append(pathway)

	return version_data