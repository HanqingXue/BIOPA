import copy
import networkx as nx 
import matplotlib.pyplot as plt


def detect_gene_family():
	fname = '../Insulin receptor signalling cascade.txt'
	g = init_graph(fname)

	degree_dist = gen_degree_dist(g)
	for degree in degree_dist.keys():
		if degree == 0:
			continue
		familys =  gen_family_base_degree(g, degree)

		'''
		Rebulid the edge
		'''
		rebulid_net(g, familys)

	f = open('new_net.txt', 'w')
	for edge in g.edges():
		f.write('{0}\t{1}\n'.format(edge[0], edge[1]))
	f.close()

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

def rebulid_net(g, familys):
	'''
	Maybe have many familys
	'''
	for family_name in familys:
		if len(familys[family_name]['target']) < 1:
			continue
		g.add_node(family_name)
		

		target = familys[family_name]['target']
		old_edges = copy.deepcopy(g.edges())
		for edge in old_edges:
			if edge[1] in target:
				g.add_edge(edge[0], family_name)
				g.remove_edge(edge[0], edge[1])
		
	return g 

if __name__ == '__main__':
	detect_gene_family()
	pass