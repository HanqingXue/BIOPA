import random
def set_node(node_id):
    node = {}
    node['data'] = {}
    node['data']['id'] = node_id
    node['data']['importance'] = 3
    node['group'] = "nodes"
    node['selected'] = False
    node['classes'] = 3 
    node['grabbable'] = True
    node['locked'] = False
    node['removed'] = False
    node['grabbed'] = False
    node['position'] = {}
    node['position']['x'] = random.randint(0, 200)
    node['position']['y'] = random.randint(0, 200)

    return node

def set_edge(source, target):
    edge = {}
    edge["group"] = "edges"
    edge["locked"] =  False
    edge["selected"] =  False
    edge["classes"] = 3
    edge["grabbable"] =  True
    edge["position"] =  {}
    edge["selectable"] =  True
    edge["removed"] = False
                
    edge['data'] = {}
    edge['data']['target'] = target
    edge['data']['source'] = source
    edge['isdirected'] = True
    edge['isdirected'] = True

    return edge