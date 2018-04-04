import random

def set_node(node_id):
    node = {}
    if '*' in node_id:
        node_id = node_id.replace('*', '_')

    node['data'] = {}
    node['data']['id'] = node_id
    node['data']['importance'] = 3
    node['group'] = "nodes"
    node['selected'] = False
    node['classes'] = 2
    node['grabbable'] = True
    node['locked'] = False
    node['removed'] = False
    node['grabbed'] = False
    node['position'] = {}
    node['position']['x'] = random.randint(0, 800)
    node['position']['y'] = random.randint(0, 800)

    return node

def set_comp_node(node_id, parent):
    node = {}
    if '*' in node_id:
        node_id = node_id.replace('*', '_')

    node['data'] = {}
    node['data']['id'] = node_id
    node['data']['importance'] = 3
    node['group'] = "nodes"
    node['selected'] = False
    node['classes'] = 2
    node['grabbable'] = True
    node['locked'] = False
    node['removed'] = False
    node['grabbed'] = False
    node['position'] = {}
    node['position']['x'] = random.randint(0, 800)
    node['position']['y'] = random.randint(0, 800)
    node['parent'] = parent

    return node

def set_edge(source, target, edge_type, path_id, path_name, manscripts, effect):
    edge = {}
    edge["group"] = "edges"
    edge["locked"] =  False
    edge["selected"] =  False
    edge["classes"] = 1
    edge["grabbable"] =  True
    edge["position"] =  {}
    edge["selectable"] =  True
    edge["removed"] = False
              
    edge['data'] = {}
    edge['data']['target'] = target
    edge['data']['source'] = source
    edge['data']['isdirected'] = True
    edge['data']["type"] = edge_type
    edge['data']['PathID'] = path_id
    edge['data']['PathName'] = path_name
    edge['data']['Manuscripts'] = manscripts
    edge['data']['Effect'] = effect

    return edge

def set_base_edge(source, target):
    edge = {}
    edge["group"] = "edges"
    edge["locked"] =  False
    edge["selected"] =  False
    edge["classes"] = 1
    edge["grabbable"] =  True
    edge["position"] =  {}
    edge["selectable"] =  True
    edge["removed"] = False
              
    edge['data'] = {}
    edge['data']['target'] = target
    edge['data']['source'] = source

    return edge


def check_node_Id(node_id):
    if '*' in node_id:
        node_id = node_id.replace('*', '_')
    return node_id