"""
author:bpt


numbers and renumbers ids
also combines files.

"""
import re
import sys
import os
import json
import pprint
sys.path.append('../../')
from utils import utilsv2 as util
from config import graph_config



unique_types = []
unique_rels = []

comment_types = ["________________________________________", "_comment", "_TODO"]

out_combined = {
    "nodes":[],
    "relationships": []
}


def create_unique_id_for_nodes (input_objs, start_no):
    """
    :param input_objs:
    :param start_no:
    :return:
    """
    current_no = start_no

    if 'nodes' in input_objs:
        for node in input_objs['nodes']:
#            if 'id' in node:
            node['id'] = current_no
            current_no = current_no + 1
            # unique adding

    return input_objs


def collect_unique_types (input_objs):
    """
    :param input_objs:
    :param start_no:
    :return:
    """

    if 'nodes' in input_objs:
        for node in input_objs['nodes']:
            # unique adding
            if 'type' in node:
                if node['type'] not in unique_types:
                    unique_types.append(node['type'])

            if 'relationships' in node:
                keys_list = list(node['relationships'].keys())
                for ind_key in keys_list:
                    if ind_key not in unique_rels:
                        unique_rels.append(ind_key)


    if 'relationships' in input_objs:
        for rel in input_objs['relationships']:
            # unique adding
            if 'type' in rel:
                if rel['type'] not in unique_rels:
                    unique_rels.append(rel['type'])

    return input_objs




def read_json_to_objects(filename):
    """
    :param input_objs:
    :param start_no:
    :return:
    """
#    print(filename)
    jsn_in_file = open(filename, 'r')
    json_txt = jsn_in_file.read()
    file_json = json.loads(json_txt)
    return file_json




if __name__ == "__main__":


    start_no = 0
    file_path = "scenario_2/"
#    filename = 'prereq.json'
#    filename = ['prereq2.json']
    filename = "out_combined.json"
    outfilename = "combined.json"


    if isinstance(filename, str):

        open_path = os.path.join(os.path.dirname(__file__),file_path)  # <-- absolute dir the script is in
    #    input_objs = read_json_to_objects(open_path + 'network.json')
        input_objs = read_json_to_objects(open_path + filename)

        # creates unique id for nodes.
        out_objs = create_unique_id_for_nodes(input_objs, start_no)
        # collects unique types
        collect_unique_types(out_objs)
        # combines multiple files into one output
        #collect_and_combine_between_files(out_objs)


    pprint.pprint(unique_types)
    pprint.pprint(unique_rels)


