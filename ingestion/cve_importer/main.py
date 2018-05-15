# Aug 2017
"""

"""
import sys
import os
import argparse
import pprint

# import local directory
from ingestion.cve_importer import collect_feed, nvd_graph_import

# patronus import
# should go to code base root dir

PATRONUS = os.environ['PYTHONPATH']
# should exist already

from utils import utilsv2 as util
from config import graph_config
from ingestion.nessus_importer import nessus_scan_ingest
from ingestion.exploitdb_importer import exploit_db_collector


if __name__ == '__main__':

    parser = argparse.ArgumentParser('Download and process VND feeds')
    #    parser.add_argument('--feed', default='recent',
    #        help='"recent" the default, "modified" or a year e.g. 2015'
    #    )

    parser.add_argument('--feed', default='2003',

                        help="""Determines the NVD feed that will be ingested.
 - 'all' - all years from 2003. Default.
 - 'recent' - recent.
 - 'modified' - recently modified.
 -  Year (eg, '2015')
 """)
    parser.add_argument('--debug', default=True, action="store_true",
                        help='displays debug comments and is verbose. '
                        )
    args = parser.parse_args()

    feed_list = []
    if args.feed == 'all':
        feed_list = ['2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011',
                     '2012', '2013', '2014', '2015', '2016', 'recent']

    else:
        feed_list.append(args.feed)

    graph = util.connect_to_graph_db(graph_config.graphDB,
                                         graph_config.graphConnectionType,
                                         graph_config.graphDBport,
                                         graph_config.username,
                                         graph_config.password)

    for year_item in feed_list:
        # Calls to retval created by nvd_20_xml function in collect feed module
        cves = collect_feed.get_nvd_feed_xml(year_item, collect_feed.process_nvd_20_xml)

        if args.debug:
            pprint.pprint(cves)
        #   util.delete_all(graph)

        try:
            nvd_graph_import.insert_nvd_cve_graph(graph, cves)
        except ImportError:
            pass

#    scan_list = [] # Starting copy of main.py line 40 to bring nessus_scan_ingest over
#    scans = nessus_scan_ingest.insert_nessus_scan_graph()
    try:
        nessus_scan_ingest.insert_nessus_scan_graph(graph)
    except Exception:
        print("Unable to import Nessus scan data")

    try:
        exploit_db_collector.download_exploit_db(graph)
    except Exception:
        print("Unable to run Exploit DB import module")
