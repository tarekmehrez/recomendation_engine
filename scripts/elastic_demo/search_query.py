# Abdelrahman

import json
import requests
import os
import math
import argparse
import sys
import logging

from elasticsearch import Elasticsearch

logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s : %(levelname)s : %(message)s')


# input arguments
parser = argparse.ArgumentParser()
parser.add_argument("query", help="add string for query")
args = parser.parse_args()


def _query(query, es):
    '''
        Performs search query

        Args:
                query(string): string which is being searched for.
                es(elasticsearch) : instance of elasticsearch connected to server.

        Returns:
                res(list): list of result dicts   
    '''
    res = es.search(index="sww", doc_type='articles', body={
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "title": query
                            }
                        },
                        {
                            "match": {
                                "content": query
                            }
                        }
                    ]
                }
            }
        })
    return res


# elastic search instantiation
our_host = 'localhost'
our_port = 9200
es = Elasticsearch([{'host': our_host, 'port': our_port}])



logging.info('Performing search query...')
# search query
query = args.query

res = _query(query, es)

#print res
#for doc in res['hits']['hits']:
    #print doc['_source']['body']

print "Number of results: " + str(len(res['hits']['hits']))
print "One result is : -----------------------"
print res['hits']['hits'][0]['_source']['title']
print res['hits']['hits'][0]['_source']['content']
