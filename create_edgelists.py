import os
from os import path
import argparse
from types import SimpleNamespace

from SPARQLWrapper import SPARQLWrapper, JSON
import networkx as nx

XSD_NAMESPACE = 'http://www.w3.org/2001/XMLSchema#'
ENDPOINT = 'http://virtuoso-midi.amp.ops.labs.vu.nl/sparql'
QUERY_DIR = './queries'
OUTPUT_DIR = './edgelist'


def main():
    all_query_files = [qf for qf in os.listdir(QUERY_DIR) if qf.endswith(".rq")]

    for query_file in all_query_files:
        query2edgelist(query_file)


def query2edgelist(query_file):
    sparql = SPARQLWrapper(ENDPOINT)

    with open(path.join(QUERY_DIR, query_file), 'r') as qf:
        query = qf.read()

        sparql.setQuery(query)
        print(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        G = nx.Graph()
        for result in results["results"]["bindings"]:
            if 'piece' in result:
                G.add_edge(to_node(result['piece']), to_node(result['event']))
            else:
                for key, value in result.items():
                    if key != 'event':
                        G.add_edge(to_node(result['event']), to_node(value))

        out_file = path.join(OUTPUT_DIR, query_file.replace(".rq", ".edgelist"))
        nx.write_edgelist(G, out_file, data=False)


def to_node(obj):
    global XSD_NAMESPACE

    type = obj['type']
    value = obj['value']

    if type == 'uri':
        return value

    if type == 'literal':
        return value.replace(" ", '_')

    if type == 'typed-literal' and obj['datatype'].startswith(XSD_NAMESPACE):
        try:
            # is a date! to half century
            decade = 5 if (int(value[3]) > 4) else 0
            return value[:2] + str(decade) + '0'
        except:
            return '_'

    return value


if __name__ == '__main__':
    main()
