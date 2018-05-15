# coding: utf-8
'''
This script downloads CVEs based on year (or recent) and then converts to a
JSON format suited for ingestion with the scenario ingestor tool.

It extracts the following:
 - CVEs
 - software versions
 - software families
 - companies
 - CVE prerequisites

The collection of data and some of the initial processing is based off:
https://gist.github.com/mountainstorm/d6baecf3cd4c500cdcc6

'''

import zipfile
import urllib.request, urllib.error, urllib.parse
import argparse
import io
import xml.etree.ElementTree as ET
import xml.etree as etree
import pprint
import re
import sys
import os
PATRONUS = os.environ['PYTHONPATH']
sys.path.append(PATRONUS)
sys.path.append(str(PATRONUS)+'/utils')
sys.path.append(str(PATRONUS)+'/config')
import utilsv2 as util
import graph_config
import json

import csv

NVD_FEEDS = {
    'recent': 'https://nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-Recent.xml.zip',
    'modified': 'https://nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-Modified.xml.zip',
    'year': 'https://nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-%s.xml.zip'
}

NAMESPACE = '{http://scap.nist.gov/schema/feed/vulnerability/2.0}'
VULN = '{http://scap.nist.gov/schema/vulnerability/0.4}'
CVSS = '{http://scap.nist.gov/schema/cvss-v2/0.2}'

BLOCKED_SOFTWARE = [
    'cpe:/h:']






def read_objects_to_json(output, o_path):
    """
    :param input_objs:
    :param start_no:
    :return:
    """
    print('outputting files')

    for k,v in output.items():
        for innerk, innerv in output[k].items():

            outdoc = o_path + os.sep + k + '_' + innerk + '.json'
            tmp_out = {}
            tmp_out['nodes'] = output[k][innerk]


            jsn_out_file = open(outdoc, 'w')
            file_json = json.dumps(tmp_out, indent=4)
            jsn_out_file.write(file_json)
#            pprint.pprint(tmp_out)

    return

# ===========================================================================================================

def clean_string(instring):
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


# ===========================================================================================================

def filter_softwares(inlist):
    """
    """
    outlist = []
    for item in inlist:
        found = False

        for sw in BLOCKED_SOFTWARE:
            if item.startswith(sw):
                found = True
        if not found:
            outlist.append(item)
    return outlist


# ===========================================================================================================

def download_nvd_feed(req_feed):
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


# ===========================================================================================================

def get_nvd_feed_xml(req_feed, callback):
    retval = {}
    retval2 = []
    try:
        feed = download_nvd_feed(req_feed)
        try:
            zip = zipfile.ZipFile(feed)
            names = zip.namelist()
            for name in names:
                try:
                    f = zip.open(name)
                    callback[0](f)
                finally:
                    f.close()
        finally:
            zip.close()
    finally:
        if feed:
            feed.close()
    return retval2

# ===========================================================================================================

def process_nvd_20_xml(xml):

    print('processing xml')

    outputs = {}
#    outputs['Ephemeral'] = {}
#    outputs['Variable'] = {}
#    outputs['Variable'][1] = []
#    outputs['Periodic'] = {}
#    outputs['Periodic'][1] = []
    outputs['Sporadic'] = {}
    outputs['Sporadic']['CVE'] = []
    outputs['Sporadic']['CVE_Prereqs'] = []
    outputs['Invariable'] = {}
    outputs['Invariable']['Company'] = []
    outputs['Invariable']['Software_Family'] = []
    outputs['Invariable']['Software_Version'] = []

    tree = ET.parse(xml)
    root = tree.getroot()
    for entry in root.findall(NAMESPACE + 'entry'):

        print('----------------')
        # process software objects
        print('  processing software objects')
        out_tmp = process_software_prereqs(entry, outputs['Invariable']['Company'], outputs['Invariable']['Software_Family'], outputs['Invariable']['Software_Version'])
        outputs['Invariable']['Company'] = outputs['Invariable']['Company'] + out_tmp['Company']
        outputs['Invariable']['Software_Family'] = outputs['Invariable']['Software_Family'] + out_tmp['Software Family']
        outputs['Invariable']['Software_Version'] = outputs['Invariable']['Software_Version'] + out_tmp['Software Version']
        # process CVEs

        print('  processing CVEs')
        temp_cve = []
        temp_cve.append(process_cve(entry, outputs['Invariable']['Software_Version']))

        # match software objects with CVEs
        print('  linking CVEs with software prerequisites')

        tmp_links = link_cves_with_software(temp_cve, outputs['Invariable']['Software_Version'])
        outputs['Sporadic']['CVE'] = outputs['Sporadic']['CVE'] + tmp_links['cve_list']
        outputs['Sporadic']['CVE_Prereqs'] = outputs['Sporadic']['CVE_Prereqs'] + tmp_links['prereq_list']


    read_objects_to_json(outputs, './')

#    pprint.pprint(outputs)
    exit()



# ===========================================================================================================

def clean_cpe_string(in_string):
    in_string = in_string.replace('_', ' ')
    if len(in_string)<4:
        in_string = in_string.upper()
    else:
        in_string = in_string.title()

    return in_string











# ===========================================================================================================

def search_internal_lists_for_matching_name(intext, inlist):
    retval = None

    for item in inlist:
        if 'name' in item:
            if item['name'] == intext:
                retval = item
    return retval


# ===========================================================================================================

def search_internal_lists_for_matching_alias(intext, inlist):
    """
    Returns an object or none if none
    :param intext:
    :param inlist:
    :return:
    """



    existing_obj = None
    for item in inlist:
#        print('searching for ')
#        print(intext)
#        print(item)
        if 'properties' in item:
#            print('in properties')
            if 'alias' in item['properties']:
#                print('in alias')
                for alias in item['properties']['alias']:
                    if alias == intext:
                        existing_obj = item
#                        print('found!')
#                        print('!!!!!!!!!!!')
#                        print(item)
    return existing_obj


# ===========================================================================================================

def process_software_prereqs(entry, existing_co_list, existing_sw_fam_list, existing_sw_v_list):

    int_entry = []
    retval = {}
    retval['Company'] = []
    retval['Software Family'] = []
    retval['Software Version'] = []




    vsw = entry.find(VULN + 'vulnerable-software-list')
    if vsw is not None:
        products = []
        for sw in vsw.iter(VULN + 'product'):
            products.append(sw.text)

        products = filter_softwares(products)
#        pprint.pprint(products)
        int_entry = products
        for sw_in in products:
            sw_in_l = sw_in.split(':')

            company = clean_cpe_string(sw_in_l[2])
            sw_type = clean_cpe_string(sw_in_l[3])
            if len(sw_in_l)<=4:
                sw_v = clean_cpe_string(sw_in_l[3])
            else:
                sw_v = clean_cpe_string(sw_in_l[4])

            company_alias = sw_in_l[0]+':'+ sw_in_l[1] + ':'+ sw_in_l[2]
            sw_fam_alias = sw_in_l[0]+':'+ sw_in_l[1] + ':'+ sw_in_l[2] + ':'+ sw_in_l[3]

            #print(sw_in)
            #print(sw_in_l)
            #print(company)
            #print(company_alias)
            #print(sw_type)
            #print(sw_fam_alias)
            #print(sw_v)

            # searches existing recent companies
            existing_co = search_internal_lists_for_matching_alias (company_alias + ' Company', retval['Company'])
            if not existing_co:
                # search pre-existing companies from other cves
                existing_co = search_internal_lists_for_matching_name(company, existing_co_list)

            if not existing_co:
                comp = {}
                comp['name'] = company + ' Company'
                comp['type'] = 'Company'
                comp['comment'] = ''
                comp['properties'] = {}
                comp['properties']['alias'] = [company_alias]
                comp['relationships'] = {}
                retval['Company'].append(comp)
                existing_co = comp

            # searches existing recent sw versions
            existing_sw_fam = search_internal_lists_for_matching_alias (sw_fam_alias, retval['Software Family'])
            if not existing_sw_fam:
                # search pre-existing sw families from other cves
                existing_sw_fam = search_internal_lists_for_matching_name(sw_type, existing_sw_fam_list)

            if not existing_sw_fam:
                sw_fam = {}
                sw_fam['name'] = sw_type
                sw_fam['type'] = 'Software Family'
                sw_fam['comment'] = ''
                sw_fam['properties'] = {}
                sw_fam['properties']['alias'] = [sw_fam_alias]
                sw_fam['relationships'] = {}
                sw_fam['relationships']['manufacturedBy'] = "name:"+existing_co['name']
                retval['Software Family'].append(sw_fam)
                existing_sw_fam = sw_fam


            existing_sw_ver = search_internal_lists_for_matching_alias (sw_in, retval['Software Version'])

            if not existing_sw_ver:
                existing_sw_ver = search_internal_lists_for_matching_alias (sw_in, existing_sw_v_list)

            if not existing_sw_ver:
                sw_ver = {}
                sw_ver['name'] = existing_sw_fam['name'] + '' + sw_v
                sw_ver['type'] = 'Software version'
                sw_ver['comment'] = ''
                sw_ver['properties'] = {}
                sw_ver['properties']['alias'] = [sw_in]
                sw_ver['properties']['version'] = sw_v
                # we don't know these.
                sw_ver['properties']['release_date'] = ''
                sw_ver['properties']['end_of_support_date'] = ''

                sw_ver['relationships'] = {}
                sw_ver['relationships']['versionOf'] = "name:"+existing_sw_fam['name']
                retval['Software Version'].append(sw_ver)
    else:
        pass


    return retval


# ===========================================================================================================


def link_cves_with_software(cve_list, existing_software_list):

    retval = {}
    retval['cve_list'] = []
    retval['prereq_list'] = []

    for cve in cve_list:
        if 'sw_prereq' in cve:
            retval['prereq_list'].append(generate_cve_prereq(cve['name'], cve['sw_prereq'], existing_software_list))
            del cve['sw_prereq']
        retval['cve_list'].append(cve)

    return retval


# ===========================================================================================================

def generate_cve_prereq(cve_name, alias_str_list, existing_sw_ver_list):

    retval = []
    prereq_no = 1
    for alias_str in alias_str_list:
        software_obj = search_internal_lists_for_matching_alias(alias_str, existing_sw_ver_list)


        if software_obj:
    #        print('*')
    #        print(software_obj)
    #        print(alias_str)
    #        print(existing_sw_ver_list)

            ret_obj = {}
            ret_obj['type'] = "CVE SW Prerequisites"
            ret_obj['comment'] = ''
            ret_obj['properties'] = {}
            ret_obj['name'] = cve_name + '_SW_Link' + str(prereq_no)

            ret_obj['relationships'] = {}
            ret_obj['relationships']['cve'] = 'name:'+ cve_name
            ret_obj['relationships']['andSWReqs'] = ['name:'+software_obj['name']]

            retval.append(ret_obj)
            prereq_no = prereq_no + 1

    return retval


# ===========================================================================================================

def process_cve(entry, existing_sw_ver_list):
    """

    :param entry:
    :param existing_sw_ver_list:
    :return:
    """
    cve = {}
    cve_props = {}
    cve_rels = {}

    cveid = entry.attrib['id']

    cve['name'] = cveid
    cve_props['vuln_id'] = []
    cve_props['vuln_id'].append(cveid)

    summary = entry.find(VULN + 'summary')
    if summary is not None and summary.text:
        cve_props['description'] = summary.text
    cve_props['date'] = entry.find(VULN + 'published-datetime').text

    references = []
    for refs in entry.iter(VULN + 'references'):
        ref = refs.find(VULN + 'reference')
        if ref is not None and 'href' in ref.attrib:
            href = ref.attrib['href']
            if len(href)>0:
                references.append(href)
    if len(references):
        cve_props['references'] = references


    vsw = entry.find(VULN + 'vulnerable-software-list')
    if vsw is not None:
        products = []
        for sw in vsw.iter(VULN + 'product'):
            products.append(sw.text)
        cve['sw_prereq'] = products
    else:
        pass

    try:
        cvss = entry.find(VULN + 'cvss')
        base_metrics = cvss.find(CVSS + 'base_metrics')
        cve_props['score'] = base_metrics.find(CVSS + 'score').text


        # access complexity
        access_complexity = base_metrics.find(CVSS + 'access-complexity').text
        if access_complexity == 'LOW':
            cve_props['complexity'] = 'Low'
        elif access_complexity == 'MEDIUM':
            cve_props['complexity'] = 'Medium'
        elif access_complexity == 'HIGH':
            cve_props['complexity'] = 'High'

        # authentication requirements
        auth_req = base_metrics.find(CVSS + 'authentication').text
        if auth_req == 'NONE':
            cve_props['authentication'] = 'None'
        elif auth_req == 'LOW':
            cve_props['authentication'] = 'Low'
        elif auth_req == 'MEDIUM':
            cve_props['authentication'] = 'Medium'
        elif auth_req == 'HIGH':
            cve_props['authentication'] = 'High'

        # vector
        vector = base_metrics.find(CVSS + 'access-vector').text
        if vector == 'NETWORK' or vector == 'ADJACENT_NETWORK':
            cve_rels['vector'] = "name:RemoteVector"
        elif vector == 'LOCAL':
            cve_rels['vector'] = "name:LocalVector"

        # confidentiality
        conf = base_metrics.find(CVSS + 'confidentiality-impact').text
        if conf == 'PARTIAL':
            cve_rels['confidentiality'] = "name:PartialImpact"
        elif conf == 'COMPLETE':
            cve_rels['confidentiality'] = "name:CompleteImpact"
        elif conf == 'NONE':
            cve_rels['confidentiality'] = "name:NoImpact"

        # availability
        avail = base_metrics.find(CVSS + 'availability-impact').text
        if avail == 'PARTIAL':
            cve_rels['availability'] = "name:PartialImpact"
        elif avail == 'COMPLETE':
            cve_rels['availability'] = "name:CompleteImpact"
        elif avail == 'NONE':
            cve_rels['availability'] = "name:NoImpact"

        # integrity
        integ = base_metrics.find(CVSS + 'integrity-impact').text
        if integ == 'PARTIAL':
            cve_rels['integrity'] = "name:PartialImpact"
        elif integ == 'COMPLETE':
            cve_rels['integrity'] = "name:CompleteImpact"
        elif integ == 'NONE':
            cve_rels['integrity'] = "name:NoImpact"

    except AttributeError:
        pass

    cve['properties'] = cve_props
    cve['relationships'] = cve_rels

#    pprint.pprint(cve)

    return cve




# ===========================================================================================================

def main(feed,
         cve_outfile,
         prereq_software_outfile = None,
         delete_on_start=False):

    # connect the graph
    graph = util.connect_to_graph_db(graph_config.graphDB,
                                     graph_config.graphConnectionType,
                                     graph_config.graphDBport,
                                     graph_config.username,
                                     graph_config.password)

    if delete_on_start:
        util.delete_all(graph)

    #
    cves = get_nvd_feed_xml('recent', [process_nvd_20_xml])





if __name__ == '__main__':

    #TODO - add arg parser
    """
    parser = argparse.ArgumentParser('Download and process VND feeds')
    #    parser.add_argument('--feed', default='recent',
    #        help='"recent" the default, "modified" or a year e.g. 2015'
    #    )
    parser.add_argument('--feed', default='2016',
                        help='"recent" the default, "modified" or a year e.g. 2015'
                        )
    args = parser.parse_args()

"""

    main('recent', True)

