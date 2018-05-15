#!/usr/bin/env python3
import random
import random
import sys
import argparse
import pprint
sys.path.append('../../config/')
import graph_config as config
sys.path.append('../../utils/')
import utils_remote as util
from py2neo import authenticate, Graph, basic_auth, GraphDatabase
from py2neo import Node, Relationship
"""
This script will find all pathes to a given depth between "entry" and the enterprise
or otherwise specified nodes on the network genereated by RNDgenerator.py
"""


def npathes(nodeType, nodeSearchProperty, entryNodeName,
                  finalNodeName, pathName, depth, __CLI__=False):
    session = util.connect_to_graph_db(config.graphDB,
                                       config.graphConnectionType,
                                       config.graphDBport,
                                       config.username, config.password)
# Find path
    entry = util.node_exists(session, nodeType,
                             nodeSearchProperty, entryNodeName)
    exit = util.node_exists(session, nodeType,
                            nodeSearchProperty, finalNodeName)
    result = util.npathes(session, entry, exit, pathName, depth)

    if __CLI__:
        for line in result:
            print(line)
    return result


def main(nodeType="Machine", nodeSearchProperty="name",
         entryNodeName="entry", finalNodeName="enterprise",
         pathName="canAttack*", depth=3, __CLI__=False):
    return npathes(nodeType, nodeSearchProperty, entryNodeName,
                         finalNodeName, pathName, depth, __CLI__=__CLI__)

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
    parser.add_argument("-d", "--depth", required=False,
                        type=int, nargs=1, default=3,
                        help="The name of the relationship which will form the path")
    args = parser.parse_args()
    nodeType = args.nodetype
    prop = args.nodeproperty
    entry = args.entryNode
    final = args.finalNode
    path = args.pathName
    depth = args.depth[0]
    null = main(nodeType, prop, entry, final, path, depth, True)
