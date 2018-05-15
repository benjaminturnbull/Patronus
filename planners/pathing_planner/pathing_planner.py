#!/usr/bin/env python3
from pprint import pprint
import sys
import time
sys.path.append("../../")
from config import graph_config as config
from utils import utils_remote as util

def find_nodes(graph, tpe="Server"):
    """
    Returns all nodes of a given type 'tpe'.
    Arguments:
        graph: The graph UID to use for the search
        tpe: the node type to search for.
    Returns:
        All nodes of given type found in the graph.
    """
    # return util.search_obj(graph, tpe)
    return util.node_exists_all(graph, tpe)


def find_local_nics(graph, node):
    """
    Finds all single hop nics from a given node 'node'.
    This is equivelant to an arp scan.
    Arguments:
        graph: The graph UID to use for the search
        node: the node object to search from.
    Returns:
        A list of nics accessable from the node.
    """
# NOTE: dont trust this code
    rels = util.match(graph, start_node=node, rel_type="hasNIC")
    ret = []
    for rel in rels:
        nicRels = util.match_through(graph, start_node=rel[1],
                                     rel1_type="onNetwork",
                                     rel2_type="onNetwork",
                                     bidirectional=True)
        for nrel in nicRels:
            ret.append(nrel[0])
    return ret

def find_server_nics(graph, node):
    """
    Finds all single hop nics from a given node 'node'.
    This is equivelant to an arp scan.
    Arguments:
        graph: The graph UID to use for the search
        node: the node object to search from.
    Returns:
        A list of nics accessable from the node.
    """
# NOTE: dont trust this code
    rels = util.match(graph, start_node=node, rel_type="hasNIC")
    ret = []
    for rel in rels:
        ret.append(rel[1])
    return ret

def find_nic_accessable_services(graph, nic, node):
    ret = []
    if "ServiceRules" not in nic or nic["ServiceRules"] == []:
        return []
    for rule in nic["ServiceRules"]:
        svc, nd = rule.split(';')
        if nd == '*' or nd.split(":")[1] == node[nd.split(":")[0]]:
            if '*' in svc:
                rels = util.match(graph, end_node=nic, rel_type="onNIC")
                for rel in rels:
                    ret.append(rel.start_node())
                return ret
            else:
                label, service = svc.split(":")
                ret.append(util.node_exists(graph, "Service", label, service))
    return ret


def find_local_services(graph, nic):
    ret = []
    for rel in util.match(graph, start_node=nic, rel_type="onNIC", bidirectional=True):
        print(type(rel[0]))
        ret.append(rel[0])
    print(ret)
    return ret


def link_machine_services(graph, node, services, rel="isVisible"):
    for svc in services:
        util.create_connection(graph, node, svc, rel)


def find_nic_accessable_nics(graph, nic, node):
    ret = []
    if "NICRules" not in nic or nic["NICRules"] == []:
        return []
    for rule in nic["NICRules"]:
        nc, nd = rule.split(';')
        if nd == '*' or nd.split(":")[1] == node[nd.split(":")[0]]:
            if '*' in nc:
                rels = util.match(graph, start_node=nic,
                                  rel_type="onNetwork", bidirectional=True)
                for rel in rels:
                    ret = list(set(ret + rel.end_node()))
                    ret = list(set(ret +
                                   find_nic_accessable_nics(graph,
                                                            rel.end_node(),
                                                            node)))
            else:
                label, service = nc.split(":")
                nic = util.node_exists(graph, "NIC", label, service)
                if nic:
                    ret = list(set(ret + nic))
                    ret = list(set(ret +
                                   find_nic_accessable_nics(graph, nic,
                                                            node)))
    return ret


def main():
    graph = util.connect_to_graph_db(config.graphDB,
                                     config.graphConnectionType,
                                     config.graphDBport,
                                     config.username, config.password)
    nodes = find_nodes(graph)
    for node in nodes:
        print("-----------------")
        pprint(node)
        print("-----------------")
        nics = find_local_nics(graph, node)
        finNics = []
        for nic in nics:
            finNics = list(set(finNics +
                               find_nic_accessable_nics(graph,
                                                        nic,
                                                        node)))
        # Merge the two lists and remove duplicates.
        d = (finNics + nics)
        finNics = [i for n, i in enumerate(d) if i not in d[n+1:]]
        # finNics = [dict(t) for t in set([tuple(sorted(d.items())) for d in (finNics + nics)])]
        services = []
        for nic in finNics:
            services = services + find_nic_accessable_services(graph, nic, node)
        services = [i for n, i in enumerate(services) if i not in services[n+1:]]
        link_machine_services(graph, node, services)
    services = find_nodes(graph, tpe="Service")


    # for each local (not subnet) nic:
    for node in nodes:
        for nic in find_server_nics(graph, node):
            localServices = []
            localServices.append(find_local_services(graph, nic))

            for service in localServices[0]:
                runningSW = util.match(graph, start_node=service, rel_type="runBySoftware")
#TODO: replace this with something more robust
                if not runningSW:
                    print("skip")
                    continue
                print("didn't skip")
                for sw in runningSW:
                    CVEs = util.match_through(graph, start_node=sw[1], rel1_type="ofSoftwareType", rel2_type="andSWReqs", bidirectional=True)
                    if not CVEs:
                        print("no CVEs")
                        continue
                    print("found CVE")
# NOTE: Not finding CVEs
                    for CVE in CVEs:
                        print("CVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVECVE")
                        pprint(CVE[0])
                        if util.trace_all_pathes(graph, CVE[0], node):
                            print("service is vulnerable")
                            util.set_node_property(graph, service, "isVulnerable", 'True')
                            util.create_connection(graph, service, CVE, "isVulnerableTo")
    for node in nodes:
        targets = util.match_property(graph, node, "isVisible", "isVulnerable", "True")
        if not targets:
            print("no targets")
            continue
        for start, end in targets:
            server = util.match_through(graph, end, "onNIC", None, "hasNIC", None, bidirectional=True)[0][0]
            pprint(server)
            util.create_connection(graph, start, server, "canExploit")
            pprint(start)
            pprint(end)


if __name__ == "__main__":
    main()

