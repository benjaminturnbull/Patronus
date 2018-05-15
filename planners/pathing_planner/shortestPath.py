#!/usr/bin/env python3
import random
import random
import sys
import argparse
import pprint
sys.path.append('../../config/')
import graph_config as config
sys.path.append('../../utils/')
sys.path.append("../../")
import utils_remote as util
from py2neo import authenticate, Graph, basic_auth, GraphDatabase
from py2neo import Node, Relationship
"""
This script will find the shortest path between "entry" and the enterprise
on the network genereated by RNDgenerator.py
"""


def shortest_path(nodeType, nodeSearchProperty, entryNodeName,
                  finalNodeName, pathName, __CLI__=False):
    session = util.connect_to_graph_db(config.graphDB,
                                       config.graphConnectionType,
                                       config.graphDBport,
                                       config.username, config.password)
# Find path
    entry = util.node_exists(session, nodeType,
                             nodeSearchProperty, entryNodeName)
    exit = util.node_exists(session, nodeType,
                            nodeSearchProperty, finalNodeName)
    result = util.shortest_path(session, entry, exit, pathName)

    if __CLI__:
        for line in result:
            print(line)
    return result


def main(nodeType="Machine", nodeSearchProperty="name",
         entryNodeName="entry", finalNodeName="enterprise",
         pathName="canAttack*", __CLI__=False):
    return shortest_path(nodeType, nodeSearchProperty, entryNodeName,
                         finalNodeName, pathName, __CLI__=__CLI__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--nodetype", required=False,
                        nargs=1, type=str, default="Machine",
                        help="The type of node to search for links between")
    parser.add_argument("-n", "--nodeproperty", required=False,
                        nargs=1, default="name",
                        help="The node property by which nodes will be found")
    parser.add_argument("-e", "--entryNode", required=False,
                        nargs=1, default="entry",
                        help="The property (by default name) to find the entry node by.")
    parser.add_argument("-f", "--finalNode", required=False,
                        nargs=1, default="enterprise",
                        help="The property (by default name) to find the final node by.")
    parser.add_argument("-p", "--pathName", required=False,
                        nargs=1, default="canAttack*",
                        help="The name of the relationship which will form the path")
    args = parser.parse_args()
    nodeType = args.nodetype[0]
    prop = args.nodeproperty[0]
    entry = args.entryNode[0]
    final = args.finalNode[0]
    path = args.pathName[0]
    main(nodeType, prop, entry, final, path, True)
