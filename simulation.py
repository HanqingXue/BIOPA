#coding=utf-8
import csv


def simulation():
	with open('network_bak.csv') as net:
		reader = csv.DictReader(net)
		version_data = []
		
		type_mapper = {}
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
			#pathway[''] = 
			version_data.append(pathway)

			if source_entity not in type_mapper.keys():
				type_mapper[source_entity] = row['shapeID1']
			else:
				continue

			if target_entity not in type_mapper.keys():
				type_mapper[target_entity] = row['shapeID2']
			else:
				continue

		mapper = open('mapper.csv', 'w')
		for key in type_mapper.keys():
			mapper.write(key + ',' + str(type_mapper[key]) + '\n')
		mapper.close() 



	return version_data

print simulation()



		