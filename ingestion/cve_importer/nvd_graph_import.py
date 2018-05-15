# coding: utf-8
'''This is a simple script to download an NVD CVE feed, extract interesting bits
from the XML and import/update a mongo db - or optionally print it to screen'''

import zipfile
import urllib.request, urllib.error, urllib.parse
import argparse
import io
import xml.etree.ElementTree as ET
import pprint
import re
import sys
import os

PATRONUS = os.environ['PYTHONPATH']
sys.path.append(PATRONUS)
PATRONUS = os.environ['PYTHONPATH']
sys.path.append(PATRONUS)

#sys.path.append(str(PATRONUS)+'/utils')
#sys.path.append(str(PATRONUS)+'/config')
from utils import utilsv2 as util
from config import graph_config
import csv

NVD_FEEDS = {
    'recent': 'https://nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-Recent.xml.zip',
    'modified': 'https://nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-Modified.xml.zip',
    'year': 'https://nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-%s.xml.zip'
}

NAMESPACE = '{http://scap.nist.gov/schema/feed/vulnerability/2.0}'
VULN = '{http://scap.nist.gov/schema/vulnerability/0.4}'
CVSS = '{http://scap.nist.gov/schema/cvss-v2/0.2}'


def write_cve_spreadsheet():
    """

    :return:
    """

    """
    myfile = open('outcsv.csv', 'w')
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)

    for item in cves:
        if 'products' in cves[item]:
            for cpeo in cves[item]['products']:
                print(cpeo)
                linelist = cpeo.split(":")
                print(type(linelist))
                print(linelist)
                wr.writerow(linelist)
"""


def clean_string(instring): # Used to return only relevant data to insert_nvd_cve
    """
    :param instring:
    :return:
    """

    outstring = re.sub(r'[^\x00-\x7f]', r'', instring)

    outstring = outstring.replace('_', ' ')

    if len(instring) > 3:
        outstring = outstring.title()
    else:
        outstring = outstring.upper()
    return outstring


def insert_nvd_cve_graph(graph, cves):
    """

    :return:
    """

    for item in cves:

        if '_id' in cves[item] and 'cvss_score' in cves[item] and 'products' in cves[item] and 'published' in cves[
            item] and 'modified' in cves[item]:

            g_cve = util.find_or_create(graph, 'Vulnerability', 'cve_id', cves[item]['_id'])
            g_cve['cvss_score'] = cves[item]['cvss_score']

            g_cve['published'] = cves[item]['published']
            g_cve['modified'] = cves[item]['modified']

            if 'summary' in cves[item]:
                g_cve['summary'] = cves[item]['summary']

            if 'products' in cves[item]:
                for cpeo in cves[item]['products']:
                    # print(cpeo)
                    linelist = cpeo.split(":")
                    if len(linelist) >= 4:
                        org = clean_string(linelist[2])
                        sw = clean_string(linelist[3])
                        if len(linelist) >= 5:
                            sw_ver = linelist[4]
                            g_org = util.find_or_create(graph, 'Organisation', 'name', org) # Creates NODE w rel values
                            g_sw = util.find_or_create(graph, 'Software', 'name', sw) # Creates NODE w rel values
                            g_sw_ver = util.find_or_create(graph, 'Software Version', 'name', sw + ' ' + sw_ver) # Node
                            g_sw_ver['version'] = sw_ver # Tacks version details on to Software Node
                            g_sw_ver['cpeid'] = cpeo # Tacks CPE info to Software Node
                            util.push(graph, g_sw_ver)
                            util.create_connection(graph, g_sw, g_org, 'manufacturer') # Creates relations sw to org
                            util.create_connection(graph, g_sw, g_sw_ver, 'software version') # relations sw to sw_ver
                            util.create_connection(graph, g_sw_ver, g_cve, 'has vulnerability') # relations sw_ver to cve
                util.push(graph, g_cve)

                sys.stdout.write('.')
                sys.stdout.flush()

# graph.merge(g_cve)
