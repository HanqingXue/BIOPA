import networkx as nx 
import matplotlib.pyplot as plt


def detect_gene_family():
	fname = '../Insulin receptor signalling cascade.txt'
	g = init_graph(fname)
	degree_dist = gen_degree_dist(g)
	print gen_family_base_degree(g, 1)

def init_graph(fname):
	pathway_records  = open(fname)
	g = nx.DiGraph()
	
	for record in pathway_records.readlines():
		record = record.strip('\n')
		record = record.split('\t')
		g.add_node(record[0])
		g.add_node(record[1])
		g.add_edge(record[0], record[1])
	return g

def gen_degree_dist(g):
	degree_dist = {}
	
	for node_id in g.nodes():
		out_degree = g.out_degree(node_id)
		if out_degree not in degree_dist:
			degree_dist[out_degree] = 1
		else:
			degree_dist[out_degree] += 1
	
	return degree_dist

def get_nodes_same_degree(g ,degree):
	nodes = []
	for record in g.out_degree():
		if record[1] == degree:
			nodes.append(record[0])
	return nodes

def f(x, y):
	return str(x) + ';' + str(y)

def gen_family_name(gene_family):
	return reduce(f, gene_family)

def gen_family_base_degree(g, degree):
	familys = {}
	for node in get_nodes_same_degree(g, degree):
		gene_family = list(g.successors(node))
		family_name = gen_family_name(gene_family)
		
		if family_name not in familys:
			familys[family_name] = {}
			familys[family_name]['num'] = 1
			familys[family_name]['target'] = gene_family
			familys[family_name]['source'] = []
			familys[family_name]['source'].append(node)
		else:
			familys[family_name]['source'].append(node)
			familys[family_name]['num'] += 1

	return familys

if __name__ == '__main__':
	detect_gene_family()
	pass