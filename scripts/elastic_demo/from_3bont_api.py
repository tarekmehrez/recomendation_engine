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


def _add_node(article, es, _id):
    '''
        Adds article's data to elasticsearch node.

        Args:
                article(dict): dict of an article containing all it's attributes.
                es(elasticsearch) : instance of elasticsearch connected to server.
                _id(int) : _id of article to be added to node.

        Returns:
                None   
    '''
    es.index(index='sww', doc_type='articles', id=_id, body={  "category": article['category'],
                                                        "title": article['title'],
                                                        "summary" : article['summary'],
                                                        "content" : article['content'],
                                                        "post_date" : article['post_date'],
                                                        "src" : article['src'],
                                                        "src_url" : article['src_url'],
                                                        "img" : article['img'],
                                                        "lang" : article['lang'],                                                        

                                                    })


# elastic search instantiation
our_host = 'localhost'
our_port = 9200
es = Elasticsearch([{'host': our_host, 'port': our_port}])

# number of pages to be fetched from 3Bont api
# pages are around 15k so far
number_of_pages = 20

_id = 1

for i in range(number_of_pages):
    logging.info("Adding nodes from page number: %s " %(i) )  
    r = requests.get('http://app2.3bont.com/api/v1/contents?page=' + str(i+1))
    data = json.loads(r.content)

    if data['data'] == []:
        break

    for article in data['data']:
        _add_node(article, es, _id)
        _id+=1









