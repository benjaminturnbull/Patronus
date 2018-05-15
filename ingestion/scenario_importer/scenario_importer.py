# coding: utf-8
"""

"""


import sys
import os
import json
import pprint
import argparse


PATRONUS = os.environ['PYTHONPATH']
sys.path.append(PATRONUS)
PATRONUS = os.environ['PYTHONPATH']
sys.path.append(PATRONUS)

#sys.path.append(str(PATRONUS)+'/utils')
#sys.path.append(str(PATRONUS)+'/config')
from utils import utilsv2 as util
from config import graph_config


def insert_node(graph, node):
    """
    """
    if 'properties' not in node:
        node['properties'] = {}
    if 'name' in node:
        node['properties']['name'] = node['name']
    if 'hostname' in node:
        node['properties']['hostname'] = node['hostname']

    node_g = util.create_object(graph, node['type'], node['properties'])
    util.push(graph, node_g)
#    util.push(graph, node_g)

    node['graph'] = node_g
    return node


def find_item_key_in_list(search_list, search_key, search_val):

    ret_item = None
    for item in search_list:
        if search_key in item:
            if item[search_key] == search_val:
                ret_item = item
                #break
                return ret_item

    for item in search_list:
        if 'properties' in item:
            if search_key in item['properties']:
                if item['properties'][search_key] == search_val:
                    ret_item = item
                    return ret_item




def insert_relationship(graph, rel, node_objects):
    """
    """
    rel['graph'] = []
    if 'properties' not in rel:
        rel['properties'] = {}

#    print('++++++')
#    print(rel)

    # if neither target or source is list
    if isinstance(rel['source'], int) and isinstance(rel['target'], int):
        node1a = find_item_key_in_list(node_objects, 'id', rel['source'])
        node1 = node1a['graph']
        node2a = find_item_key_in_list(node_objects, 'id', rel['target'])
        node2 = node2a['graph']

#        print(node1)
#        print(node2)

        rel_g = util.create_connection(graph, node1, node2, rel['type'])
        rel['graph'].append(rel_g)

    # if source is list, target not.
    elif isinstance(rel['source'], list) and isinstance(rel['target'], int):
        for source_item in rel['source']:
            node1a = find_item_key_in_list(node_objects, 'id', source_item)
            node1 = node1a['graph']
            node2a = find_item_key_in_list(node_objects, 'id', rel['target'])
            node2 = node2a['graph']
            rel_g = util.create_connection(graph, node1, node2, rel['type'], propertydict=rel['properties'], allow_dup=False)
#            graph.push(rel_g)
            rel['graph'].append(rel_g)

    # if target is list, source not.
    elif isinstance(rel['source'], int) and isinstance(rel['target'], list):
        for target_item in rel['target']:
            node1a = find_item_key_in_list(node_objects, 'id', rel['source'])
            node1 = node1a['graph']
            node2a = find_item_key_in_list(node_objects, 'id', target_item)
            node2 = node2a['graph']
            rel_g = util.create_connection(graph, node1, node2, rel['type'], propertydict=rel['properties'], allow_dup=False)
#            graph.push(rel_g)
            rel['graph'].append(rel_g)

    # if both source and target are lists
    elif isinstance(rel['source'], list) and isinstance(rel['target'], list):
        for source_item in rel['source']:
            for target_item in rel['target']:
                node1a = find_item_key_in_list(node_objects, 'id', source_item)
                node1 = node1a['graph']
                node2a = find_item_key_in_list(node_objects, 'id', target_item)
                node2 = node2a['graph']
                rel_g = util.create_connection(graph, node1, node2, rel['type'], propertydict=rel['properties'], allow_dup=False)
#                graph.push(rel_g)
                rel['graph'].append(rel_g)
    else:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(rel)

    return rel




def insert_internal_relationship (srcnode, node_objects, rel_type, dst_string, graph):

    if isinstance(dst_string, str):
        dst_type = dst_string[0:dst_string.find(":")]
        dst_name = dst_string[dst_string.find(":")+1:]

        dstnode = find_item_key_in_list(node_objects, dst_type, dst_name)
        srcnode = srcnode['graph']
        dstnode = dstnode['graph']

        rel_g = util.create_connection(graph, srcnode, dstnode, rel_type, allow_dup=False)
        util.push(graph, rel_g)

    elif isinstance(dst_string, list):

        for actual_str in dst_string:
            dst_type = actual_str[0:actual_str.find(":")]
            dst_name = actual_str[actual_str.find(":")+1:]

            dstnode = find_item_key_in_list(node_objects, dst_type, dst_name)
            srcnodea = srcnode['graph']
            dstnodea = dstnode['graph']

            rel_g = util.create_connection(graph, srcnodea, dstnodea, rel_type, allow_dup=False)
            util.push(graph, rel_g)
            util.push(graph, rel_g)


def insert_into_graph (graph, inputs):
    """

    :return:
    """
    node_objects = []
    rel_objects = []



    if 'nodes' in inputs:



        for node in inputs['nodes']:

            if "_comment" not in node:

                if 'id' in node and 'type' in node:
                    tmpnode = insert_node(graph, node)
                    node_objects.append(tmpnode)
                    insert_node(graph, node)
#                    sys.stdout.write(',')
                    sys.stdout.flush()

                    if 'relationships' in node:
                        for rla in node['relationships']:
#                            print('insert rel')
#                            print(rla)
#                            print(node['relationships'][rla])

                            insert_internal_relationship(tmpnode, node_objects, rla, node['relationships'][rla], graph)
#                            sys.stdout.write('.')
                            sys.stdout.flush()
            else:
                print(node)

    if 'relationships' in inputs:
        for rel in inputs['relationships']:
            if 'source' in rel and 'target' in rel and 'type' in rel:
                print('insert rel')
                print(rel)
                rel_objects.append(insert_relationship(graph, rel, node_objects))
#                sys.stdout.write('.')
                sys.stdout.flush()
            else:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(rel)


def read_json_to_objects(filename):
    jsn_in_file = open(filename, 'r')
    json_txt = jsn_in_file.read()
    file_json = json.loads(json_txt)
    return file_json




def main(prerequisite_path, prerequisite_files, scenario_path, scenario_files, delete_on_start=True):

# connect the graph
    graph = util.connect_to_graph_db(graph_config.graphDB,
                                     graph_config.graphConnectionType,
                                     graph_config.graphDBport,
                                     graph_config.username,
                                     graph_config.password)

    if delete_on_start:
        util.delete_all(graph)

# handle prerequisite files
    open_path = os.path.join(os.path.dirname(__file__), prerequisite_path)
    print('handling prerequisites')
    for indi_filename in prerequisite_files:
        input_objs = read_json_to_objects(open_path + indi_filename)
        insert_into_graph(graph, input_objs)

# handle scenario files
    open_path = os.path.join(os.path.dirname(__file__), scenario_path)
    print('handling scenarios')
    for indi_filename in scenario_files:
        input_objs = read_json_to_objects(open_path + indi_filename)
        insert_into_graph(graph, input_objs)

if __name__ == "__main__":

# TODO put a command line option in
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers',
                        metavar='N',
                        type=int,
                        nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print(args.accumulate(args.integers))
    """

    prerequisite_path = "scenario_2/prerequisites/"
    prerequisite_files = []
    scenario_path = "scenario_2/"
    scenario_files = ['out_combined.json']
    delete_on_start = True

    main(prerequisite_path, prerequisite_files, scenario_path, scenario_files, delete_on_start)

