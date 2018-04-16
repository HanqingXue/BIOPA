import networkx as nx

g = nx.Graph()

f = open('p53net.txt')

for item in f.readlines():
	print item
	item = item.split('\t')
	print item
	g.add_node(item[0])
	g.add_node(item[1])
	g.add_edge(item[0], item[1])

g