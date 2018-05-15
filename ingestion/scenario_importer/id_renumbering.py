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


def create_unique_id_for_nodes(input_objs, start_no):
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

    if 'relationships' in input_objs:
        for rel in input_objs['relationships']:
            # unique adding
            if 'type' in rel:
                if rel['type'] not in unique_rels:
                    unique_rels.append(rel['type'])

    return input_objs


def collect_and_combine_between_files (input_objs, start_no=0):
    """
    :param input_objs:
    :param start_no:
    :return:
    """
    current_no = start_no

    if 'nodes' in input_objs:
        for node in input_objs['nodes']:
            if "_comment" not in node and "________________________________________" not in node:
                if 'id' in node and 'type' in node and 'name' in node:
                    out_combined['nodes'].append(node)
                elif 'type' in node and 'name' in node:
                    node['id'] = 0
                    out_combined['nodes'].append(node)

                else:
                    print('=================================')
                    print('FAILED NODE')
                    pprint.pprint(node)
                    print('=================================')
                    exit()

    if 'relationships' in input_objs:
        for rel in input_objs['relationships']:
            if 'source' in rel and 'type' in rel and 'target' in rel:
                out_combined['relationships'].append(rel)
            else:
                print('=================================')
                print('FAILED RELATIONSHIP')
                pprint.pprint(rel)
                print('=================================')

    return input_objs





def read_json_to_objects(filename):
    """
    :param input_objs:
    :param start_no:
    :return:
    """
    print(filename)
    jsn_in_file = open(filename, 'r')
    json_txt = jsn_in_file.read()
    file_json = json.loads(json_txt)
    return file_json



def read_objects_to_json(objs, o_path,  filename):
    """
    :param input_objs:
    :param start_no:
    :return:
    """
    filename_out = "out_" + filename
    outdoc = o_path + filename_out

    print("&&&&&&&&&&&&&&&&&&&&&&&&")
    print(filename_out)
    print(objs)

    jsn_out_file = open(outdoc, 'w')
    file_json = json.dumps(objs, indent=4)
#    file_json = json.dumps(objs, indent=4, sort_keys=True)
    jsn_out_file.write(file_json)
#    pprint.pprint(objs)
    return


def main(file_path, filename, outfilename, start_no=0):

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

        read_objects_to_json(out_objs, open_path, filename)

    elif isinstance(filename, list):

        open_path = os.path.join(os.path.dirname(__file__), file_path)  # <-- absolute dir the script is in
        #    input_objs = read_json_to_objects(open_path + 'network.json')

        for indi_filename in filename:
            input_objs = read_json_to_objects(open_path + indi_filename)

            # creates unique id for nodes.
            out_objs = create_unique_id_for_nodes(input_objs, start_no)
            # collects unique types
            collect_unique_types(out_objs)
            # combines multiple files into one output
            collect_and_combine_between_files(out_objs)

        read_objects_to_json(out_combined, open_path, outfilename)

    pprint.pprint(unique_types)
    pprint.pprint(unique_rels)



if __name__ == "__main__":

    start_no = 0
    file_path = "scenario_2/"
#    filename = 'prereq.json'
#    filename = ['prereq2.json']
    filename = ['prereq.json','prereq2.json', 'network.json', 'auth.json']
    outfilename = "combined.json"

    main(file_path, filename, outfilename, start_no=0)
