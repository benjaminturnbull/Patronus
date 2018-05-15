#!/usr/bin/env python3
import sys
sys.path.append("../")
from config import graph_config as config
from utils import utils_remote as util


print(config.graphDB)
print(config.graphConnectionType)
print(config.graphDBport)
print(config.username)
print(config.password)

graph = util.connect_to_graph_db(config.graphDB, config.graphConnectionType, config.graphDBport, config.username, config.password)
print(graph)
nodes = util.orphan_nodes(graph)
for node in list(nodes):
    print(node)

