
import sys
from pprint import pprint
sys.path.append('../config/')
# import config
import uuid
import random
from py2neo import authenticate, Graph, NodeSelector
from py2neo import Node, Relationship

graphs = {}
def find_or_create (graph, nodeType, propertyname, propertyvalue):
    """
    :param graph:
    :param propertyname:
    :param propertyvalue:
    :return:
    """
    resp = None
    resp = node_exists(graph, nodeType, propertyname, propertyvalue)
    if not resp:
        resp = create_object(graph, nodeType, {propertyname: propertyvalue, 'Node Type': nodeType})
    return resp

def create_object(graph, atype, propertiesdict):
    """
    creates a generic object
    """
    graph = graphs[graph]
    if 'Unique ID' not in propertiesdict:
        propertiesdict['Unique ID'] = str(uuid.uuid4())
#    if 'thing1' not in propertiesdict:
#        propertiesdict['thing2'] = atype
#    if 'label' not in propertiesdict:
#        propertiesdict['thing3'] = atype

#    tmpnode = Node(type, propertiesdict)
    tmpnode = Node(atype, id=propertiesdict['Unique ID'])

#    print(propertiesdict)
    for k in propertiesdict:
        tmpnode[k] = propertiesdict[k]
#    print (type(tmpnode))
#    print(dict(tmpnode))
#    print(type(propertiesdict))
#    exit()
    graph.create(tmpnode)
    graph.push(tmpnode)
    tmpnode["nodeType"] = list(tmpnode.labels())[0]
    return tmpnode

def node_exists(graph, nodeType, propertyname, propertyvalue):
    """
    Check if a node exists given it's type and label
    On success will return the node.
    On failure, will return none
    """
    graph = graphs[graph]
    #TODO: rewrite this using NodeSelector, find_one is deprecated.

    # print('debug')
    # print(propertyname)
    # print(propertyvalue)
    selector = NodeSelector(graph)

    #TODO: Test this!
    # search1 = selector.select(nodeType).where("_."+propertyname+"="+propertyvalue).first()

    search1 = graph.find_one(nodeType, property_key=propertyname, property_value=propertyvalue)
    if search1:
        search1["nodeType"] = list(search1.labels())[0]
        return search1
    else:
        return None


def node_exists_label_in_list(graph, nodeType, propertyname, propertyvalue, **kwargs):
    """
    Check if a node exists given:
     - type
     - a property of type list:
     - a value to search for in it
    On success will return the node.
    On failure, will return none
    """
    graph = graphs[graph]

    selector = NodeSelector(graph)
    search1 = selector.select(nodeType)

    if search1:
        search_res = list(search1)
        for ind_res in search_res:
            if propertyname in ind_res:
                for ind_prop in ind_res[propertyname]:
                    if ind_prop == propertyvalue:
                        ind_res["nodeType"] = list(ind_res.labels())[0]
                        return ind_res
        return None
    else:
        return None


def node_exists_all(graph, nodeType, **kwargs):
    """
    Check if a node exists given it's type and label
    On success will return the node.
    On failure, will return none
    """
    graph = graphs[graph]

    selector = NodeSelector(graph)
#    print(graph)
#    print(nodeType)
#    print(kwargs)
    search1 = selector.select(nodeType) #, kwargs)
    if search1:
        ret = []
        for item in list(search1):
            item["nodeType"] = list(item.labels())[0]
            ret.append(item)
        return ret
    else:
        return None

def search_obj(graph, nodeType):
    """
    Check if a node exists given it's type and label
    On success will return the node.
    On failure, will return none
    """
    graph = graphs[graph]

    search1 = graph.find(nodeType)
    if search1:
        ret = []
        for item in list(search1):
            item["nodeType"] = list(item.labels())[0]
            ret.append(item)
        return ret
    else:
        print ('poop')
        return None


def search_rel(graph, relType):
    """
    Check if a node exists given it's type and label
    On success will return the node.
    On failure, will return none
    """
    graph = graphs[graph]

    # print('debug')
    # print(propertyname)
    # print(propertyvalue)

    search1 = graph.find(relType)
    if search1:
        return search1
    else:
        print ('poop')
        return None

def delete_all(graph):
    """
    delete all objects in the session
    """
    graph = graphs[graph]
    graph.delete_all()

def connect_to_graph_db(graphDB, graphConnectionType, graphDBport, username, password):
    """
    Connects to graph DB
    """
    authenticate(graphDB +
                 ':' +
                 str(graphDBport),
                 username,
                 password)
    uid = str(uuid.uuid4())
    graphs[uid] = Graph(graphConnectionType +
                         '://' +
                         graphDB +
                         ':' +
                         str(graphDBport) +
                         "/db/data/")
    return uid

def merge(graph, subgraph, label=None, *args):
    #TODO: This is far too low level to have in the util.
    graph = graphs[graph]
    graph.merge(subgraph, args, label=label)

def push(graph, subgraph):
    #TODO: This is far too low level to have in the util.
    graph = graphs[graph]
    graph.push(subgraph)

def match(graph, start_node=None, rel_type=None, end_node=None, bidirectional=False, limit=None):
    graph = graphs[graph]
    ret = []
    for item in graph.match(start_node=start_node, rel_type=rel_type,
                            end_node=end_node, bidirectional=bidirectional,
                            limit=limit):
        start_node, end_node = item.nodes()
        start_node["nodeType"] = list(start_node.labels())[0]
        end_node["nodeType"] = list(end_node.labels())[0]
        ret.append([dict(start_node), dict(end_node)])
    return ret


def match_property(graph, start_node, rel_type, end_property_name, end_property_value, bidirectional=False, limit=None):
    graph = graphs[graph]
    ret = []
    q = "MATCH (s:" + start_node["nodeType"] + "{id: '" + start_node["id"] + "'})-[:" + rel_type + "]-(e:Service {" + end_property_name + ": '" + end_property_value + "'})" + \
        " return s, e"
    ret = graph.run(q)
    paths = []
    for path in ret:
        node1, node2 = path
        node1["nodeType"] = list(node1.labels())[0]
        node2["nodeType"] = list(node2.labels())[0]
        paths.append((node1, node2))
    pprint(paths)
    print(q)
    return paths


def match_through(graph, start_node=None, rel1_type=None, mid_node=None, rel2_type=None, end_node=None, bidirectional=False, limit=None):
    graph = graphs[graph]
    query = ""
    if not start_node:
        query = "MATCH (s)-[r1"
    else:
        query = "MATCH (s: " + start_node["nodeType"] + "{id: '" + start_node["id"] + "'})-[r1"
    if not rel1_type:
        query += "]-" + ">(" if bidirectional else "("
    else:
        query += ":" + rel1_type + "]-" + "(" if bidirectional else ">("
    if not mid_node:
        query += "m)-[r2"
    else:
        query += "m: " + mid_node["nodeType"] + "{id: '" + mid_node["id"] + "'})-[r2"
    if not rel2_type:
        query += "]-" + "(" if bidirectional else ">("
    else:
        query += ":" + rel2_type + "]-" + "(" if bidirectional else ">("
    if not end_node:
        query += "e)"
    else:
        query += "e: " + end_node["nodeType"] + "{id: '" + end_node["id"] + "'})"
    query += " RETURN e"
    if limit:
        query += " LIMIT " + str(limit)

    ret = graph.run(query)
    return list(ret)





def connection_exists(graph, node1, node2, linktype):
    """

    :param graph:
    :param node1:
    :param node2:
    :param linktype:
    :return:
    """
    graph = graphs[graph]
    if len(list(graph.match(start_node=node1, end_node=node2, rel_type=linktype))) > 0:
        return True
    else:
        return False

def create_connection(graph, node1, node2, linktype, propertydict=None, allow_dup=False):
    """

    :param graph:
    :param node1:
    :param node2:
    :param linktype:
    :param propertydict:
    :return:
    """
    graph = graphs[graph]
    anode = node1
    bnode = node2

    if isinstance(node1, dict):
        if 'type' in node1 and 'id' in node1:
            anode = node_exists(graph, node1['type'], 'id', node1['id'])
            if not anode:
                print('failed to make new connection - node a cannot be found')
                return

    if isinstance(node2, dict):
        if 'type' in node2 and 'id' in node2:
            bnode = node_exists(graph, node2['type'], 'id', node2['id'])
            if not bnode:
                print('failed to make new connection - node b cannot be found')
                return

    if len(list(graph.match(start_node=anode, end_node=bnode, rel_type=linktype))) == 0 and allow_dup is False:

        if propertydict:
            newrel = Relationship(anode, linktype, bnode)
            graph.create(newrel)
            graph.push(newrel)
            return newrel

        else:
            newrel = Relationship(anode, linktype, bnode)
            graph.create(newrel)
            graph.push(newrel)
            return newrel
    else:
        # print('rel already exists')
        return

def get_graph(graph):
    graph = graphs[graph]
    q = "match (n) return n"
    resp = graph.run(q)
    return resp


def shortest_path(graph, entryNode, exitNode, linkType):
    graph = graphs[graph]
    q = "match (start:" + entryNode["nodeType"] + " {name: '" + entryNode["name"] +\
        "'}), (end:" + exitNode["nodeType"] + " {name: '" + exitNode["name"] + "'})," +\
        " p=shortestPath((start)-[:" + linkType + "]->(end)) return p"
    ret = graph.run(q)
    path = []
    out = ret.data()[0]['p']
    for node in out.nodes():
        node["nodeType"] = list(node.labels())[0]
        path.append(node)
    return path


def all_shortest_pathes(graph, entryNode, exitNode, linkType, depth):
    graph = graphs[graph]
    q = "match (start:" + entryNode["nodeType"] + " {name: '" + entryNode["name"] +\
        "'}), (end:" + exitNode["nodeType"] + " {name: '" + exitNode["name"] + "'})," +\
        " p=allShortestPaths((start)-[:" + linkType + ".." + str(depth) + "]->(end)) return p"
    ret = graph.run(q)
    pathes = []
    out = ret.data()
    for path in out:
        p = []
        for node in path['p'].nodes():
            node["nodeType"] = list(node.labels())[0]
            p.append(node)
        pathes.append(p)
    return pathes


def npathes(graph, entryNode, exitNode, linkType, depth):
    graph = graphs[graph]
    q = "match (start:" + entryNode["nodeType"] + " {name: '" + entryNode["name"] +\
        "'}), (end:" + exitNode["nodeType"] + " {name: '" + exitNode["name"] + "'})," +\
        "p=(start)-[:" + linkType + ".." + str(depth) + "]->(end) return p"
    ret = graph.run(q)
    pathes = []
    out = ret.data()
    for path in out:
        p = []
        for node in path['p'].nodes():
            node["nodeType"] = list(node.labels())[0]
            p.append(node)
        pathes.append(p)
    return pathes

def orphan_nodes(graph):
    graph = graphs[graph]
    q = "MATCH (n) where not (n)-[]-() return n"
    ret = graph.run(q)
    return list(ret)


def trace_all_pathes(graph, from_node, end_node):
    graph = graphs[graph]
    # This gives us everything we need to check whether all pathes were followed.
    # The value of rel2 should match that of len(p)
    q = "MATCH p=(a:`CVE SW Prerequisites` {id: '" + from_node['id'] + "'})-[r:andSWReqs]-()-[r1:ofSoftwareType]-()-[r2:runsSoftware]-(e:Server {id: '" +  end_node["id"] + """'})
           optional MATCH (a)-[x:andSWReqs]-()
           with p, count(x) as rel2
           return p, rel2"""
    ret = list(graph.run(q))
    pathes = []
    for path in ret:
        if path['rel2'] == len(ret):
            pathes.append((path['p'].start_node(), path['p'].end_node()))
    return pathes
def delete_orphans(graph):
    graph = graphs[graph]
    q = "MATCH (n) where not (n)-[]-() delete n"
    graph.run(q)


def set_node_property(graph, node, property_name, property_value):
    graph = graphs[graph]
    graph.merge(node)
    node[property_name] = property_value
    node.push()
