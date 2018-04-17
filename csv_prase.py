#coding=utf-8
import csv

def simulation():
	with open('network_bak.csv') as net:
		reader = csv.DictReader(net)
		version_data = []
		
		for row in reader:
			pathway = {}
			source_entity = row['ID1']
			target_entity = row['ID2']
			interaction = 'MI'
			pathway['Entity1'] = source_entity
			pathway['Entity2'] = target_entity
			pathway['Interaction'] = interaction
			pathway['PathID'] = 'ipa'
			pathway['PathName'] = 'ipa'
			pathway['ManuscriptID'] = '21900206;21900206|imex:IM-16799'
			pathway['Effect'] = 'null'
			version_data.append(pathway)

	return version_data



		