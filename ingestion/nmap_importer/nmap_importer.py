#!/usr/bin/env python3

import nmap as nm
import pprint
import argparse


def nmap_scan(outDir, address, flags="-A"):
    """
    Scan the target CIDR address using Nmap.
    The flags "-A -oX" are used by default.
    Arguments:
        outDir: The directory to place output files in.
        flags: A string of nmap flags, excluding host and output flags or None.
        address: The address (in bare or CIDR format) to be scanned if not using hosts.
    Returns:
        nmap: A python-nmap object to interpret the nmap XML output.
        Output in XML format also written to <outDir>/nmap.xml.
    """
    nmap = {}
    nmap = nm.PortScanner()
    nmap.scan(address, arguments=flags)
    with open(outDir + "nmap.xml", 'w') as outFile:
        outFile.write(nmap.get_nmap_last_output())
    return nmap


def create_structure():
    output = {}
    output["nodes"] = []
    return output


def add_hosts(nmap, output):
    swlist = []
    swverlist = []
    niclist = []
    hostlist = []
    for host in nmap.all_hosts():
        try:
            server = {}
            server["name"] = nmap[host].hostname()
            server["type"] = "Server"
            server["comment"] = ""
            server["id"] = 1
            server["relationships"] = {}
            server["relationships"]["runsSoftware"] = []
            ports = nmap[host]["tcp"]
            keys = list(ports)
            for port in keys:
                sw = {}
                swver = {}
                sw["name"] = ports[port]["product"]
                sw["type"] = "Software Family"
                sw["comment"] = ""
                sw["properties"] = {}
                sw["relationships"] = {"manufacturedBy": ""}
                sw["id"] = 23
                if sw not in swlist:
                    swlist.append(sw)
                swver["name"] = sw["name"] + " " + ports[port]["version"]
                swver["type"] = "Software version",
                swver["comment"] = ""
                swver["properties"] = {
                    "version": ports[port]["version"],
                    "release_date": "",
                    "end_of_support_date": ""
                },
                swver["relationships"] = {
                    "versionOf": "name:" + sw["name"]
                },
                swver["id"] = 37
                if swver not in swverlist:
                    swverlist.append(swver)
                server["relationships"]["runsSoftware"].append("name:" + swver["name"])
            # for i in range(0, len(list(nmap[host]["addresses"]["ipv4"]))):
            nic = {}
            nic["name"] = nmap[host].hostname() + " NIC "
            nic["type"] = "NIC"
            nic["properties"] = {
                    "ipAddress": nmap[host]["addresses"]["ipv4"],
                    "macAddress": ""
                    }
            nic["id"] = 1
            niclist.append(nic)
            server["relationships"]["hasNIC"] = "name:" + nic["name"]
            hostlist.append(server)
            for item in swlist:
                output["nodes"].append(item)
            for item in swverlist:
                output["nodes"].append(item)
            for item in hostlist:
                output["nodes"].append(item)
            for item in niclist:
                output["nodes"].append(item)
        except Exception as e:
            print(e)
            continue
    return output


def main(target):
    nmap = nmap_scan("./", target)
    output = create_structure()
    output = add_hosts(nmap, output)
    pprint.pprint(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", required=True, nargs=1,
                        help="The address to scan. Use CIDR notation")
    args = parser.parse_args()
    target = args.address[0]
    main(target)
