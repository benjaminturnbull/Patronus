#!/usr/bin/env python3
"""



"""
import pprint
import argparse
import csv
import json



def create_structure():
    output = {}
    output["nodes"] = []

    return output


def read_file_to_object(filename):
    """
    :param filename:
    :return: dictreader output
    """
    print(filename)
    input_file = csv.DictReader(open(filename))
    return input_file

def read_objects_to_json(objs, filename_out):
    """
    :param input_objs:
    :param start_no:
    :return:
    """
    jsn_out_file = open(filename_out, 'w')
    file_json = json.dumps(objs, indent=4)
    jsn_out_file.write(file_json)
    return

def parse_cwes(input_file, collectFiler, verbose=False):
    """
    :param input_file: the file in dictreader output
    :param collectFiler: read input args
    :param verbose: add additional detail
    :return: list of cwe dicts
    """
    return_list = []

    for row in input_file:
        cwe_obj = {}
        cwe_prop = {}
        cwe_obj['type'] = "CWE"
        cwe_obj['name'] = "CWE"+row["ID"]
        cwe_obj['comment'] = row["Name"]

        #add properties
        cwe_prop['label'] = "CWE " + str(row["ID"])
        cwe_prop['cwe id'] = row["ID"]
        if verbose:
            cwe_prop['status'] = row["Status"]
            cwe_prop['description'] = row["Description"]

        cwe_obj['properties'] = cwe_prop
        # TODO - add these in with relationships
        #    Related Weaknesses
        #    Weakness Ordinalities
        #    Taxonomy Mappings
        #    Related Attack Patterns

        if collectFiler == 1:
            if row["Status"] == "Class":
                return_list.append(cwe_obj)
        elif collectFiler == 2:
            if row["Status"] == "Base":
                return_list.append(cwe_obj)
        elif collectFiler == 3:
            if row["Status"] == "Variant":
                return_list.append(cwe_obj)
        else:
            return_list.append(cwe_obj)

    return return_list



def main(file_path, filters, outpath):

    cwe_list_obj = read_file_to_object(file_path)
    out_cwe_form = parse_cwes(cwe_list_obj, filters)
    output_obj = create_structure()
    output_obj['nodes'] = out_cwe_form

    if outpath == False:
        pprint.pprint(output_obj)
    else:
        read_objects_to_json(output_obj, outpath)



if __name__ == "__main__":
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True, nargs=1,
                        help="File path of cwe csv taken from https://cwe.mitre.org/data/index.html")
    parser.add_argument("-c", "--collect-filter", required=False, nargs=1,
                        help="filer is either 'class'=1, 'base'=2, 'variant'=3 or 'all'=4")
    parser.add_argument("-o", "--out", required=False, nargs=1,
                        help="out filepath and filename. If not present, will pretty print")
    args = parser.parse_args()


    file_path = args.address[0]
    collectFilter = args.address[1]
    outfile = args.address[2]


    main(file_path, collectFilter, )
    """
    main('/Users/bpt/Code/Patronus/data/cwe/699.csv', 4, '/Users/bpt/Code/Patronus/data/cwe/out_699.json')
    main('/Users/bpt/Code/Patronus/data/cwe/1000.csv', 4, '/Users/bpt/Code/Patronus/data/cwe/out_1000.json')
    main('/Users/bpt/Code/Patronus/data/cwe/1008.csv', 4, '/Users/bpt/Code/Patronus/data/cwe/out_1008.json')
