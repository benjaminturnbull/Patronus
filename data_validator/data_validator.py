'''

author: bpt
'''

import random
import uuid
import json
import sys

from neo4j.v1 import GraphDatabase, basic_auth

sys.path.append('../config/')
import graph_config
import object_forms

sys.path.append('../utils/')
import utils

internal_objects ={}


def objectTester(node_type, record):
    type_exists = False
    errorcode = ''
    errorlist =[]
#    print(node_type)

    for evaltype in object_forms.objects:
        if evaltype['name'] == node_type:
            type_exists = True

            for evaltype_object_type in evaltype:
                failedTest = False

# tests go here.

# Does item exist
                if evaltype[evaltype_object_type] == '':
                    failedTest = True
                    errorcode = '\tMissing required object'
                    for node in record["n"]:
                        if node == evaltype_object_type:
                            failedTest = False

# Does item belong to acceptable list
                elif type(evaltype[evaltype_object_type]) == list:
                    failedTest = True
                    errorcode = '\tObject is not in list'
                    for node in record["n"]:
                        if node == evaltype_object_type:
                            for eval_option in evaltype[evaltype_object_type]:
                                if eval_option == record['n'][node]:
                                    failedTest = False

                if failedTest:
                    print('ERROR in Object')
                    print (errorcode)
                    print('\t'+str(record) + '')

    if not type_exists:
        print('ERROR File Does Not Exist')
        print(errorcode)
        print('\t' + str(record) + '')

    return type_exists


'''
'''
def runtestquery(session):
    q = """MATCH (n) RETURN n;"""
    resp = session.run(q)

    for record in resp:
        # yes this is a bastardisation but I can't find an easy way to return the type
        rec_Str = str(record['n'])
        rec_Str = rec_Str[rec_Str.find('labels={') + 9:]
        rec_Str = rec_Str[:rec_Str.find('}') - 1]

        objectTester(rec_Str, record)


'''
main method
'''
if __name__ == "__main__":
    driver = GraphDatabase.driver(graph_config.graphDB, auth=basic_auth(graph_config.username, graph_config.password))
    session = driver.session()

    runtestquery(session)

    session.close()
    exit()
