#!/usr/bin/python3

import json
import argparse
from pprint import pprint

types = []
def main(target, comments):
    content = None
    try:
        with open(target) as inFile:
            content = json.loads(inFile.read())
    except:
        print("File not found or does not contain JSON")
        exit(1)
    print("Checking existance of nodes: {}".format("\033[94mPASSED\033[0m"
          if checkNodesExist(content) else "\033[91mFAILED\033[0m"))
    print("Checking node content: {}".format("\033[94mPASSED\033[0m"
          if checkNodeContent(content["nodes"], comments) else "\033[91mFAILED\033[0m"))
    print("Checking node properties: {}".format("\033[94mPASSED\033[0m"
          if checkNodeProperties(content["nodes"]) else "\033[91mFAILED\033[0m"))
    print("Checking node relationships: {}".format("\033[94mPASSED\033[0m"
          if checkNodeRelationships(content["nodes"]) else "\033[91mFAILED\033[0m"))
    print("Checking Data Time Classification: {}".format("\033[94mPASSED\033[0m"
          if checkDataVariability(content["nodes"]) else "\033[91mFAILED\033[0m"))


def checkNodesExist(content):
    return "nodes" in content



def checkNodeContent(nodes, comments):
    ret = True
    nodeContent = {"name": str, "type": str,
                   "properties": dict, "id": int}
    if comments:
        nodeContent["comment"] = str
    for node in nodes:
        if "________________________________________" in node:
            continue
        if "_comment" in node:
            continue
        for key, value in nodeContent.items():
            if key not in node:
                ret = False
                print("\033[91m{} not in node:\033[0m\n".format(key))
                pprint(node)
                print("\n------------------------------------------\n")
            elif type(node[key]) is not value:
                ret = False
                print("\033[91mtype of node ({}) is not correct {}:\033[0m\n".format(type(node[key]), value))
                pprint(node)
                print("\n------------------------------------------\n")
        try:
            if node["type"] not in types:
                types.append(node["type"])
        except KeyError as e:
            print("Could not add node to type list. Does the node have a type?")
            pprint(node)
            print(e)
    return ret


def checkNodeProperties(nodes):
    ret = True
    properties = {}
    properties["NIC"] = {"ipAddress": str, "macAddress": str, "NICRules": str, "ServiceRules": str}
    properties["Firewall"] = {"runsSoftware": list, "hasNIC": list}
    properties["Service"] = {"port": int}
    properties["Reported Vulnerability"] = {"vuln_id": list, "date": str, "description": str,
                                            "references": str, "score": float, "complexity": str,
                                            "authentication": str, "attackTypes": list}
    properties["Protocol"] = {"version": str, "defaultPorts": list}
    properties["DataClassification"] = {"classification": list}
    properties["other"] = {}
    for node in nodes:
        if "________________________________________" in node:
            continue
        if "_comment" in node:
            continue
        try:
            if node["type"] not in properties.keys():
                for key, value in properties["other"].items():
                    if key not in node["properties"]:
                        ret = False
                        print("\033[91m{} property expected but not found in node\n\033[0m".format(key))
                        pprint(node)
                        print("\n------------------------------------------\n")
                    # next statement checks that we are restricting the content of the property
                    elif type(value) is list and node["properties"][key] not in value:
                        ret = False
                        print("\033[91m{} set as {} in node is not an allowable value:\033[0m\n".format(node["properties"][key], key))
                        pprint(node)
                        print("\n------------------------------------------\n")
                continue

            for tpe, props in properties.items():
                if node["type"] == tpe:
                    for key, value in props.items():
                        if key not in node["properties"]:
                            ret = False
                            print("\033[91m{} property expected but not found in node\n\033[0m".format(key))
                            pprint(node)
                            print("\n------------------------------------------\n")
                        # next statement checks that we are restricting the content of the property
                        elif type(value) is list and node["properties"][key] not in value:
                            ret = False
                            print("\033[91m{} set as {} in node is not an allowable value:\033[0m\n".format(node["properties"][key], key))
                            pprint(node)
                            print("\n------------------------------------------\n")
            if node["type"] == "NIC":
                for rule in node["properties"]["NICRules"]:
                    if ";" not in rule:
                            ret = False
                            print("\033[91m{} All firewall rules must contain a ; demiliter\n\033[0m".format(rule))
                            pprint(node)
                            print("\n------------------------------------------\n")
                for rule in node["properties"]["ServiceRules"]:
                    if ";" not in rule:
                            ret = False
                            print("\033[91m{} All firewall rules must contain a ; demiliter\n\033[0m".format(rule))
                            pprint(node)
                            print("\n------------------------------------------\n")

        except KeyError as e:
            ret = False
            print("Could not test node due to improper fromatting, This issues is likely found in the output of checkNodeContent()")
            pprint(node)
            pprint(e)


    return ret


def checkNodeRelationships(nodes):
    ret = True
    relationships = {}
    relationships["workstation"] = {"runsSoftware": list, "hasNIC": list}
    relationships["server"] = {"runsSoftware": list, "hasNIC": list}
    relationships["Firewall"] = {"runsSoftware": list, "hasNIC": list}
    relationships["Service"] = {"runBySoftware": list, "onNIC": list,
                                "runsProtocol": list}
    relationships["RunningSoftware"] = {"ofSoftwareType": list}
    relationships["Route"] = {"routeSystem": list, "routeSource": list,
                              "routePort": list, "destinationService": list,
                              "hasNIC": list}
    relationships["Exploit"] = {"exploitsVulnerability": list, "softwareModuleOf": list,
                                "requiresService": list, "requiresCPUArchitecture": list}
    relationships["Reported Vulnerability"] = {"confidentiality": str, "integrity": str,
                                               "availability": str, "prerequisites": list,
                                               "outcomes": list, "CWEs": list, "vector": list}
    relationships["DataTimeClassification"] = {"dataFormClassifications": list}
    relationships["CVE SW Prerequisites"] = {"cve": str, "andSWReqs": list, "notSWReqs": list}
    for node in nodes:
        if "________________________________________" in node:
            continue
        if "_comment" in node:
            continue
        try:
            for tpe, rels in relationships.items():
                if node["type"] == tpe:
                    for key, value in rels.items():
                        if key not in node["relationships"]:
                            ret = False
                            print("\033[91m{} relationship expected but not found in node\033[0m\n".format(key))
                            pprint(node)
                            print("\n------------------------------------------\n")
                        elif type(node["relationships"][key]) is not value:
                            ret = False
                            print("\033[91mexpected relationship listing {} to have type {}\033[0m\n".format(key, value))
                            pprint(node)
                            print("\n------------------------------------------\n")
                        else:
                            if value is list:
                                for rel in node["relationships"][key]:
                                    if ":" not in rel:
                                        ret = False
                                        print("\033[91mExpected property name in relationship {}\033[0m\n".format(rel))
                                        pprint(node)
                                        print("\n------------------------------------------\n")
                            else:
                                if ":" not in node["relationships"][key]:
                                    ret = False
                                    print("\033[91mExpected property name in relationship {}\033[0m\n".format(rel))
                                    pprint(node)
                                    print("\n------------------------------------------\n")
        except KeyError as e:
            ret = False
            print("Could not test node due to improper fromatting, This issues is likely found in the output of checkNodeContent()")
            pprint(node)
            pprint(e)

    return ret


def checkDataVariability(nodes):
    ret = True
    tps = []
    for node in nodes:
        try:
            if node["type"] == "DataTimeClassification":
                expectedRels = ["name:EphemeralDataForms",
                                "name:VariableDataForms",
                                "name:PeriodicDataForms",
                                "name:SporadicDataForms",
                                "name:InvariableDataForms"]
                for rel in expectedRels:
                    if rel not in node["relationships"]["dataFormClassifications"]:
                        print("\033[91mMissing classification relationship:\033[0m {}".format(rel))
                        ret = False
        except KeyError:
            continue

        if node["type"] == "DataClassification":
            try:
                dtc = node["properties"]["classification"]
            except KeyError as e:
                print("\033[91mMalformed node properties:\033[0m")
                pprint(node)
                print(e)
                print("\033[91mThis was probably reported in the properties check above.\033[0m")
                continue

            for item in dtc:
                if item in tps:
                    print("\033[91mItem has been classified twice:\033[0m {}".format(item))
                    continue
                tps.append(item)
    tmpTypes = types[:]  # Python uses references behind my back...
    for nodeType in types:
        if nodeType in tps:
            tps.remove(nodeType)
            tmpTypes.remove(nodeType)

    if tmpTypes:
        print("\033[91mThe following types were not classified by DataTimeClassifiaction\033[0m")
        pprint(tmpTypes)
        ret = False
    if tps:
        print("\033[91mThe following types were found in DataTimeClassification, but are unused\033[0m")
        pprint(tps)
        ret = False
    return ret


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True, nargs=1,
                        help="JSON file to check")
    parser.add_argument("-c", "--comments", required=False,
                        action="store_true", default=False,
                        help="Alert on missing comments")
    args = parser.parse_args()
    target = args.file[0]
    main(target, args.comments)
