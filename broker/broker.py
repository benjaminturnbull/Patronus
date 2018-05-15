#!/usr/bin/python3
from flask import Flask, request, jsonify
import json
from pprint import pprint
import sys
sys.path.append('../utils/')
import utilsv2 as util

app = Flask(__name__)
BASEURL = "/patronus/v1/"


@app.route(BASEURL + "find_or_create", methods=['GET', 'POST'])
def find_or_create():
    args = request.get_json()
    if (not args["graph"] or
        not args["nodeType"] or
        not args["propertyname"] or
        not args["propertyvalue"]):
            return json.dumps({"error": "Invalid arguments"}), 400
    ret = util.find_or_create(args["graph"], args["nodeType"],
            args["propertyname"], args["propertyvalue"])
    ret = dict(ret) # This happens at the jsonify stage anyway
    ret["type"] = args["nodeType"] # Only way to store the type
    resp = jsonify(ret)
    resp.status_code=200
    resp = jsonify(ret)
    resp.status_code=200
    return resp


@app.route(BASEURL + "create_object", methods=['POST'])
def create_object():
    args = request.get_json()
    if (not args["graph"] or
        not args["atype"] or
        not args["propertiesdict"]):
            return json.dumps({"error": "Invalid arguments"}), 400
    ret = util.create_object(args["graph"], args["atype"],
            args["propertiesdict"])
    resp = jsonify(ret)
    resp.status_code=200
    return resp


@app.route(BASEURL + "node_exists", methods=['GET'])
def node_exists():
    args = request.get_json()
    if (not args["graph"] or
        not args["nodeType"] or
        not args["propertyname"] or
        not args["propertyvalue"]):
            return json.dumps({"error": "Invalid arguments"}), 400
    ret = util.node_exists(args["graph"], args["nodeType"],
            args["propertyname"], args["propertyvalue"])
    resp = jsonify(ret)
    resp.status_code=200
    return resp


@app.route(BASEURL + "node_exists_all", methods=['GET'])
def node_exists_all():
    args = request.get_json()
    if (not args["graph"] or
        not args["nodeType"]):
            return json.dumps({"error": "Invalid arguments"}), 400
    if "kwargs" in args:
        ret = util.node_exists_all(args["graph"], args["nodeType"],
                kwargs=args["kwargs"])
    else:
        ret = util.node_exists_all(args["graph"], args["nodeType"])
    for node in ret:
        node["nodeType"] = args["nodeType"]
    resp = jsonify(ret)
    resp.status_code=200
    return resp


@app.route(BASEURL + "search_obj", methods=['GET'])
def search_obj():
    args = request.get_json()
    if (not args["graph"] or
        not args["nodeType"]):
            return json.dumps({"error": "Invalid arguments"}), 400
    ret = util.search_obj(args["graph"], args["nodeType"])
    resp = jsonify(ret)
    resp.status_code=200
    return resp


@app.route(BASEURL + "search_rel", methods=['GET'])
def search_rel():
    args = request.get_json()
    if (not args["graph"] or
        not args["relType"]):
            return json.dumps({"error": "Invalid arguments"}), 400
    ret = util.search_rel(args["graph"], args["relType"])
    resp = jsonify(ret)
    resp.status_code=200
    return resp


@app.route(BASEURL + "delete_all", methods=['GET'])
def delete_all():
    args = request.get_json()
    if not args["graph"]:
            return json.dumps({"error": "Invalid arguments"}), 400
    ret = util.delete_all(args["graph"])
    resp = jsonify(ret)
    resp.status_code=200
    return resp


@app.route(BASEURL + "connect_to_graph_db", methods=['GET'])
def connect_to_graph_db():
    args = request.get_json()
    if (not args["graphDB"] or
        not args["graphConnectionType"] or
        not args["graphDBport"] or
        not args["username"] or
        not args["password"]):
            return json.dumps({"error": "Invalid arguments"}), 400
    ret = util.connect_to_graph_db(args["graphDB"],
            args["graphConnectionType"], args["graphDBport"],
            args["username"], args["password"])
    resp = jsonify(ret)
    resp.status_code=200
    return resp


# To be removed
@app.route(BASEURL + "merge", methods=['POST'])
def merge():
    args = request.get_json()
    if (not args["graph"] or
        not args["subgraph"]):
            return json.dumps({"error": "Invalid arguments"}), 400
    ret = util.merge(args["graph"],
            args["subgraph"], args["args"] or None,
            args["label"] or None)
    resp = jsonify(ret)
    resp.status_code=200
    return resp


# To be removed
@app.route(BASEURL + "push", methods=['POST'])
def push():
    args = request.get_json()
    if (not args["graph"] or
        not args["subgraph"]):
            return json.dumps({"error": "Invalid arguments"}), 400
    ret = util.push(args["graph"],
            args["subgraph"])
    resp = jsonify(ret)
    resp.status_code=200
    return resp


@app.route(BASEURL + "match", methods=['GET'])
def match():
    args = request.get_json()
    if not args["graph"]:
            return json.dumps({"error": "Invalid arguments"}), 400
    if "start_node" in args and args["start_node"]:
        node1 = util.node_exists(args["graph"], args["start_node"]["nodeType"], "id", args["start_node"]["id"])
    else:
        node1 = None
    if "end_node" in args and args["end_node"]:
        node2 = util.node_exists(args["graph"], args["end_node"]["nodeType"], "id", args["end_node"]["id"])
    else:
        node2 = None
    ret = util.match(args["graph"],
                     start_node=(node1 or None),
                     rel_type=(args["rel_type"] or None),
                     end_node=(node2 or None),
                     bidirectional=(args["bidirectional"] or False),
                     limit=(args["limit"] or None))
    resp = jsonify(ret)
    resp.status_code=200
    return resp


@app.route(BASEURL + "match_property", methods=['GET'])
def match_property():
    args = request.get_json()
    if (not args["graph"] or
        not args["start_node"] or
        not args["rel_type"] or
        not args["end_property_name"] or
        not args["end_property_value"]):
            return json.dumps({"error": "Invalid arguments"}), 400
    if "start_node" in args and args["start_node"]:
        node1 = util.node_exists(args["graph"], args["start_node"]["nodeType"], "id", args["start_node"]["id"])
    else:
        node1 = None
    ret = util.match_property(args["graph"],
                              node1,
                              args["rel_type"],
                              args["end_property_name"],
                              args["end_property_value"],
                              bidirectional=(args["bidirectional"] or False),
                              limit=(args["limit"] or None))
    resp = jsonify(ret)
    resp.status_code = 200
    return resp


@app.route(BASEURL + "match_through", methods=['GET'])
def match_through():
    args = request.get_json()
    if not args["graph"]:
            return json.dumps({"error": "Invalid arguments"}), 400
    if "start_node" in args and args["start_node"]:
        node1 = util.node_exists(args["graph"], args["start_node"]["nodeType"], "name", args["start_node"]["name"])
    else:
        node1 = None
    if "mid_node" in args and args["mid_node"]:
        node2 = util.node_exists(args["graph"], args["mid_node"]["nodeType"], "name", args["mid_node"]["name"])
    else:
        node2 = None
    if "end_node" in args and args["end_node"]:
        node3 = util.node_exists(args["graph"], args["end_node"]["nodeType"], "name", args["end_node"]["name"])
    else:
        node3 = None
    ret = util.match_through(args["graph"],
            start_node=(node1 or None),
            rel1_type=(args["rel1_type"] or None),
            mid_node=(node2 or None),
            rel2_type=(args["rel2_type"] or None),
            end_node=(node3 or None),
            bidirectional=(args["bidirectional"] or False),
            limit=(args["limit"] or None))
    resp = jsonify(ret)
    resp.status_code = 200
    return resp

@app.route(BASEURL + "trace_all_pathes", methods=['GET'])
def trace_all_pathes():
    args = request.get_json()
    if not args["graph"] or \
        not args["start_node"] or\
        not args["end_node"]:
            return json.dumps({"error": "Invalid arguments"}), 400
    if "start_node" in args and args["start_node"]:
        node1 = util.node_exists(args["graph"], args["start_node"]["nodeType"], "name", args["start_node"]["name"])
    else:
        node1 = None
    if "end_node" in args and args["end_node"]:
        node3 = util.node_exists(args["graph"], args["end_node"]["nodeType"], "name", args["end_node"]["name"])
    else:
        node3 = None
    ret = util.trace_all_pathes(args["graph"],
                             node1, node3)
    resp = jsonify(ret)
    resp.status_code = 200
    return resp



@app.route(BASEURL + "connection_exists", methods=['GET'])
def connection_exists():
    args = request.get_json()
    if (not args["graph"] or
        not args["node1"] or
        not args["node2"] or
        not args["linkType"]):
            return json.dumps({"error": "Invalid arguments"}), 400
    ret = util.connection_exists(args["graph"],
            args["node1"], args["node2"], args["linktype"])

    resp = jsonify({"connected": ret})
    resp.status_code = 200 if ret else 500
    return resp


@app.route(BASEURL + "create_connection", methods=['POST'])
def create_connection():
    # This needs to find the nodes, sending their dicts doesn't work.
    args = request.get_json()
    node1 = util.node_exists(args["graph"], args["node1"]["nodeType"], "id", args["node1"]["id"])
    node2 = util.node_exists(args["graph"], args["node2"]["nodeType"], "id", args["node2"]["id"])

    if (not args["graph"] or
        not node1 or
        not node2 or
        not args["linktype"]):
            return json.dumps({"error": "Invalid arguments"}), 400
    ret = util.create_connection(args["graph"],
            node1, node2, args["linktype"],
            propertydict=(args["propertydict"] or None),
            allow_dup=(args["allow_dup"] or False))
    if str(ret):
        resp = jsonify({"connected": True})
        return resp, 200
    else:
        resp = jsonify({"connected": False})
        return resp, 500


@app.route(BASEURL + "get_graph", methods=['GET'])
def get_graph():
    args = request.get_json()
    if not args["graph"]:
            return json.dumps({"error": "Invalid arguments"}), 400
    ret = util.get_graph(args["graph"])
    resp = jsonify(ret)
    resp.status_code=200
    return resp


@app.route(BASEURL + "shortest_path", methods=['GET'])
def shortest_path():
    args = request.get_json()
    if (not args["graph"] or
        not args["entryNode"] or
        not args["exitNode"] or
        not args["linkType"]):
            return json.dumps({"error": "Invalid arguments"}), 400
    ret = util.shortest_path(args["graph"], args["entryNode"],
                             args["exitNode"], args["linkType"])
    resp = jsonify(ret)
    resp.status_code = 200
    return resp


@app.route(BASEURL + "all_shortest_pathes", methods=['GET'])
def all_shortest_pathes():
    args = request.get_json()
    if (not args["graph"] or
        not args["entryNode"] or
        not args["exitNode"] or
        not args["depth"] or
        not args["linkType"]):
            return json.dumps({"error": "Invalid arguments"}), 400
    ret = util.all_shortest_pathes(args["graph"], args["entryNode"],
                             args["exitNode"], args["linkType"], args["depth"])
    resp = jsonify(ret)
    resp.status_code = 200
    return resp


@app.route(BASEURL + "npathes", methods=['GET'])
def npathes():
    args = request.get_json()
    if (not args["graph"] or
        not args["entryNode"] or
        not args["exitNode"] or
        not args["depth"] or
        not args["linkType"]):
            return json.dumps({"error": "Invalid arguments"}), 400
    ret = util.npathes(args["graph"], args["entryNode"],
                       args["exitNode"], args["linkType"], args["depth"])
    resp = jsonify(ret)
    resp.status_code = 200
    return resp


@app.route(BASEURL + "orphan_nodes", methods=['GET'])
def orphan_nodes():
    args = request.get_json()
    if (not args["graph"]):
            return json.dumps({"error": "Invalid arguments"}), 400
    ret = util.orphan_nodes(args["graph"])
    resp = jsonify(ret)
    resp.status_code = 200
    return resp


@app.route(BASEURL + "delete_orphans", methods=['GET'])
def delete_orphans():
    args = request.get_json()
    if (not args["graph"]):
            return json.dumps({"error": "Invalid arguments"}), 400
    util.orphan_nodes(args["graph"])
    resp = jsonify("OK")
    resp.status_code = 200
    return resp

@app.route(BASEURL + "set_node_property", methods=['POST'])
def set_node_property():
    args = request.get_json()
    if (not args["graph"] or
        not args["node"] or
        not args["property_name"] or
        not args["property_value"]):
            return json.dumps({"error": "Invalid arguments"}), 400

    if "node" in args and args["node"]:
        node1 = util.node_exists(args["graph"], args["node"]["nodeType"], "id", args["node"]["id"])
    else:
        return json.dumps({"error": "Invalid arguments"}), 400
    util.set_node_property(args["graph"], node1, args["property_name"], args["property_value"])
    return "OK", 200


if __name__ == '__main__':
    app.run(debug=True)
