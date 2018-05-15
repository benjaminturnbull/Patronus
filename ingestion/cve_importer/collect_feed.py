# Aug 2017
# coding: utf-8
"""

Downloads CVE NVD feeds and converts to a useful format.
This script has been adapted from:


"""

import zipfile
import urllib.request, urllib.error, urllib.parse
import argparse
import io
import xml.etree.ElementTree as ET
import pprint
import re
import sys


NVD_FEEDS = {
    'recent': 'https://nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-Recent.xml.zip',
    'modified': 'https://nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-Modified.xml.zip',
    'year': 'https://nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-%s.xml.zip'
}

NAMESPACE = '{http://scap.nist.gov/schema/feed/vulnerability/2.0}'
VULN = '{http://scap.nist.gov/schema/vulnerability/0.4}'
CVSS = '{http://scap.nist.gov/schema/cvss-v2/0.2}'


def download_nvd_feed(req_feed): # Retrieves the NVDCVE data from URL's and sticks data in retval
    retval = None
    # download the feed
    feed = None
    if req_feed in NVD_FEEDS and req_feed != 'year':
        feed = NVD_FEEDS[req_feed]
    else:
        try:
            feed = NVD_FEEDS['year'] % int(req_feed)
        except ValueError:
            pass  # not a number
    if feed is not None:
        print('info: downloading %s' % feed)
        retval = io.BytesIO(urllib.request.urlopen(feed).read())

    return retval


def get_nvd_feed_xml(req_feed, callback): # Calls download_nvd_feed function and creates dictionary
    retval = {}
    try:
        feed = download_nvd_feed(req_feed)
        print ('FEED')
        print(feed)
        try:
            zip = zipfile.ZipFile(feed) # unzipping data from the feed into zip var
            names = zip.namelist() #
            for name in names:
                try:
                    f = zip.open(name)
                    retval.update(callback(f))
                finally:
                    f.close()
        finally:
            zip.close()
    finally:
        if feed:
            feed.close()
    return retval


def process_nvd_20_xml(xml):
    retval = {}
    tree = ET.parse(xml)
    root = tree.getroot()
    for entry in root.findall(NAMESPACE + 'entry'):
        cveid = entry.attrib['id']
        if cveid not in retval:

            # print(type(entry))
            # print(entry)

            cve = {'_id': cveid}
            summary = entry.find(VULN + 'summary')
            if summary is not None and summary.text:
                cve['summary'] = summary.text

            cve['published'] = entry.find(VULN + 'published-datetime').text
            cve['modified'] = entry.find(VULN + 'last-modified-datetime').text

            vsw = entry.find(VULN + 'vulnerable-software-list')
            if vsw is not None:
                products = []
                for sw in vsw.iter(VULN + 'product'):
                    products.append(sw.text)
                cve['products'] = products
            else:
                # print("!!!!!")
                pass

            try:
                cvss = entry.find(VULN + 'cvss')
                base_metrics = cvss.find(CVSS + 'base_metrics')
                cve['cvss_score'] = base_metrics.find(CVSS + 'score').text
            except AttributeError:
                pass

            references = []
            for refs in entry.iter(VULN + 'references'):
                ref = refs.find(VULN + 'reference')
                if ref is not None and 'href' in ref.attrib:
                    href = ref.attrib['href']
                    text = ref.text
                    if href is not None:
                        if text is None:
                            text = href
                        references.append({'href': href, 'description': text})
            if len(references):
                cve['references'] = references
            retval[cveid] = cve
    return retval

