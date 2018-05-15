import sys
import uuid
import random
import requests
import json

sys.path.append('../config/')
sys.path.append('../')
from config import graph_config as config

def find_or_create (graph, nodeType, propertyname, propertyvalue):
    """
    :param graph:
    :param propertyname:
    :param propertyvalue:
    :return:
    """
    data = {}
    data["graph"] = graph
    data["nodeType"] = nodeType
    data["propertyname"] = propertyname
    data["propertyvalue"] = propertyvalue
    resp = requests.get(config.APIURL + config.APIBaseURL + "find_or_create", json=data)
    if resp.status_code == 200:
            ret = resp.json()
    else:
        ret = None
    print("find or create")
    # TODO: ret will likely need to be altered
    return ret

def create_object(graph, atype, propertiesdict):
    """
    creates a generic object
    """
    data = {}
    data["graph"] = graph
    data["atype"] = atype
    data["propertiesdict"] = propertiesdict
    resp = requests.post(config.APIURL + config.APIBaseURL + "create_obj", json=data)
    tmpnode = None
    if resp.status_code == 200:
            tmpnode = resp.json()
    print("create object")
    return tmpnode

def node_exists(graph, nodeType, propertyname, propertyvalue):
    """
    Check if a node exists given it's type and label
    On success will return the node.
    On failure, will return none
    """
    data = {}
    data["graph"] = graph
    data["nodeType"] = nodeType
    data["propertyname"] = propertyname
    data["propertyvalue"] = propertyvalue
    resp = requests.get(config.APIURL + config.APIBaseURL + "node_exists", json=data)
    search1 = None
    if resp.status_code == 200:
            search1 = resp.json()
    # search1 = graph.find_one(nodeType, property_key=propertyname, property_value=propertyvalue)
    if search1:
        search1["nodeType"] = nodeType
        return search1
    else:
        return None

def node_exists_all(graph, nodeType, **kwargs):
    """
    Check if a node exists given it's type and label
    On success will return the node.
    On failure, will return none
    """

    data = {}
    data["graph"] = graph
    data["nodeType"] = nodeType
    data["kwargs"] = kwargs
    resp = requests.get(config.APIURL + config.APIBaseURL + "node_exists_all", json=data)
    search1 = None
    if resp.status_code == 200:
            search1 = resp.json()
    if search1:
        return search1
    else:
        return None

def search_obj(graph, nodeType):
    """
    Check if a node exists given it's type and label
    On success will return the node.
    On failure, will return none
    """

    data = {}
    data["graph"] = graph
    data["nodeType"] = nodeType
    resp = requests.get(config.APIURL + config.APIBaseURL + "search_obj", json=data)
    search1 = None
    if resp.status_code == 200:
            search1 = resp.json()
    if search1:
        return search1
    else:
        print ('poop')
        return None

def search_rel(graph, relType):
    """
    Check if a node exists given it's type and label
    On success will return the node.
    On failure, will return none
    """

    data = {}
    data["graph"] = graph
    data["relType"] = relType
    resp = requests.get(config.APIURL + APIBaseURL + "search_rel", json=data)
    search1 = None
    if resp.status_code == 200:
            search1 = resp.json()
    print("search Rel")
    if search1:
        return search1
    else:
        print ('poop')
        return None

def delete_all(graph):
    """
    delete all objects in the session
    """
    resp = requests.get(config.APIURL + config.APIBaseURL + "delete_all", data=(json.dumps({"data": graph})))
    if resp.status_code == 200:
            ret = resp.json()
    else:
        ret = None
    print("delete all")
    return ret

def connect_to_graph_db(graphDB, graphConnectionType, graphDBport, username, password):
    """
    Connects to graph DB
    """
    data = {}
    data["graphDB"] = graphDB
    data["graphConnectionType"] = graphConnectionType
    data["graphDBport"] = graphDBport
    data["username"] = username
    data["password"] = password
    resp = requests.get(config.APIURL + config.APIBaseURL + "connect_to_graph_db",
                        json=data)
    if resp.status_code == 200:
        ret = resp.json()
    else:
        ret = None
    print("connect to graph db")
    return ret

def merge(graph, subgraph, label=None, *args):
    #TODO: This is far too low level to have in the util.
    data = {}
    data["graph"] = graph
    data["subgraph"] = subgraph
    data["label"] = label
    data["args"] = args
    resp = requests.post(config.APIURL + config.APIBaseURL + "merge", json=data)
    if resp.status_code == 200:
            ret = resp.json()
    else:
        ret = None
    print("merge")
    return ret

def push(graph, subgraph):
    #TODO: This is far too low level to have in the util.
    data = {}
    data["graph"] = graph
    data["subgraph"] = subgraph
    resp = requests.post(config.APIURL + config.APIBaseURL + "push", json=data)
    if resp.status_code == 200:
            ret = resp.json()
    else:
        ret = None
    print("push")
    return ret

def create(graph, subgraph):

    #TODO: This is far too low level to have in the util.
    data = {}
    data["graph"] = graph
    data["subgraph"] = subgraph
    resp = requests.post(config.APIURL + config.APIBaseURL + "create", json=data)
    if resp.status_code == 200:
            ret = resp.json()
    else:
        ret = None
    print("create")
    return ret


def match(graph, start_node=None, rel_type=None, end_node=None, bidirectional=False, limit=None):
    data = {}
    data["graph"] = graph
    data["start_node"] = start_node
    data["rel_type"] = rel_type
    data["end_node"] = end_node
    data["bidirectional"] = bidirectional
    data["limit"] = limit
    resp = requests.get(config.APIURL + config.APIBaseURL + "match", json=data)
    if resp.status_code == 200:
            ret = resp.json()
    else:
        ret = None
    print("match")
    return ret

def match_property(graph, start_node, rel_type, end_property_name, end_property_value, bidirectional=False, limit=None):
    data = {}
    data["graph"] = graph
    data["start_node"] = start_node
    data["rel_type"] = rel_type
    data["end_property_name"] = end_property_name
    data["end_property_value"] = end_property_value
    data["bidirectional"] = bidirectional
    data["limit"] = limit
    resp = requests.get(config.APIURL + config.APIBaseURL + "match_property", json=data)
    if resp.status_code == 200:
            ret = resp.json()
    else:
        ret = None
    print("match_property")
    return ret


def match_through(graph, start_node=None, rel1_type=None, mid_node=None, rel2_type=None, end_node=None, bidirectional=False, limit=None):
    data = {}
    data["graph"] = graph
    data["start_node"] = start_node
    data["rel1_type"] = rel1_type
    data["mid_node"] = mid_node
    data["rel2_type"] = rel2_type
    data["end_node"] = end_node
    data["bidirectional"] = bidirectional
    data["limit"] = limit
    resp = requests.get(config.APIURL + config.APIBaseURL + "match_through", json=data)
    if resp.status_code == 200:
            ret = resp.json()
    else:
        ret = None
    print("match_through")
    return ret

def connection_exists(graph, node1, node2, linktype):
    """

    :param graph:
    :param node1:
    :param node2:
    :param linktype:
    :return:
    """
    data = {}
    data["graph"] = graph
    data["node1"] = node1
    data["node2"] = node2
    data["linktype"] = linktype
    resp = requests.get(config.APIURL + config.APIBaseURL + "connection_exists", json=data)
    if resp.status_code == 200:
        ret = resp.json()
    else:
        ret = None
    print("connection exists")
    return ret

def trace_all_pathes(graph, start_node, end_node):
    """

    :param graph:
    :param node1:
    :param node2:
    :param linktype:
    :return:
    """
    data = {}
    data["graph"] = graph
    data["start_node"] = start_node
    data["end_node"] = end_node
    resp = requests.get(config.APIURL + config.APIBaseURL + "trace_all_pathes", json=data)
    if resp.status_code == 200:
        ret = resp.json()
    else:
        ret = None
    print("trace_all_pathes")
    return ret


def create_connection(graph, node1, node2, linktype, propertydict=None, allow_dup=False):
    """


    :param graph:
    :param node1:
    :param node2:
    :param linktype:
    :param propertydict:
    :return:
    """
    data = {}
    data["graph"] = graph
    data["node1"] = node1
    data["node2"] = node2
    data["linktype"] = linktype
    data["propertydict"] = propertydict
    data["allow_dup"] = allow_dup
    resp = requests.post(config.APIURL + config.APIBaseURL + "create_connection", json=data)
    if resp.status_code == 200:
            ret = resp.json()
    else:
        ret = None
    print("create connection")
    return ret

def get_graph(graph):
    data = {}
    data["graph"] = graph
    resp = requests.get(config.APIURL + config.APIBaseURL + "get_graph", json=data)
    if resp.status_code == 200:
            ret = resp.json()
    else:
        ret = None
    print("get Graph")
    return ret

def shortest_path(graph, entryNode, exitNode, linkType):
    data = {}
    data["graph"] = graph
    data["entryNode"] = entryNode
    data["exitNode"] = exitNode
    data["linkType"] = linkType
    resp = requests.get(config.APIURL + config.APIBaseURL + "shortest_path", json=data)
    if resp.status_code == 200:
            ret = resp.json()
    else:
        ret = None
    print("shortest_path")
    return ret


def all_shortest_pathes(graph, entryNode, exitNode, linkType, depth):
    data = {}
    data["graph"] = graph
    data["entryNode"] = entryNode
    data["exitNode"] = exitNode
    data["linkType"] = linkType
    data["depth"] = depth
    resp = requests.get(config.APIURL + config.APIBaseURL + "all_shortest_pathes", json=data)
    if resp.status_code == 200:
            ret = resp.json()
    else:
        ret = None
    return ret


def npathes(graph, entryNode, exitNode, linkType, depth):
    data = {}
    data["graph"] = graph
    data["entryNode"] = entryNode
    data["exitNode"] = exitNode
    data["linkType"] = linkType
    data["depth"] = depth
    resp = requests.get(config.APIURL + config.APIBaseURL + "npathes", json=data)
    if resp.status_code == 200:
            ret = resp.json()
    else:
        ret = None
    return ret


def orphan_nodes(graph):
    data = {}
    data["graph"] = graph
    resp = requests.get(config.APIURL + config.APIBaseURL + "orphan_nodes", json=data)
    if resp.status_code == 200:
        ret = resp.json()
    else:
        ret = None
    return ret

def delete_orphans(graph):
    data = {}
    data["graph"] = graph
    requests.get(config.APIURL + config.APIBaseURL + "orphan_nodes", json=data)


def set_node_property(graph, node, property_name, property_value):
    data = {}
    data["graph"] = graph
    data["node"] = node
    data["property_name"] = property_name
    data["property_value"] = property_value
    requests.post(config.APIURL + config.APIBaseURL + "set_node_property", json=data)
