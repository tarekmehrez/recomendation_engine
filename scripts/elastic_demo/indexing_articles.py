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

def _get_article(rootdir):
    """
        Opens all .txt files and adds them to a list.

        Args:
                rootdit(str): path of root director.

        Returns:
                list(str): list of articles
    """
    articles = []
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            path = os.path.join(subdir, file)
            file = open(path, 'r')
            text = ' '.join(file)
            articles.append(text)

    return articles


# elastic search instantiation
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# getting list of all articles
logging.info('Grabbing articles...')
rootdir = '../rec_engine/data/en/2016-06-22/'
articles = _get_article(rootdir)

print str(len(articles)) + " articles found"

logging.info('Adding indices...')
i = 0
# loop to add article nodes
for article in articles:
    es.index(index='sw', doc_type='articles', id=i, body={"body":article, "title": "SUCCESS"})
    # print entry
    i+=1

# trying to get nodes
#print es.get(index='sw', doc_type='articles', id=2)['_source']['body']
#print es.get(index='sw', doc_type='articles', id=2)['_source']['title']


logging.info('Performing search query...')
# search query
query = args.query
res = es.search(index="sw", doc_type='articles', body={"query": {"match" : { "body" : query}}})

#print res
#for doc in res['hits']['hits']:
    #print doc['_source']['body']

print "Number of results: " + str(len(res['hits']['hits']))
print "One result is : -----------------------"
print res['hits']['hits'][0]['_source']['body']



