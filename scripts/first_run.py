# Abdelrahman

import os
import logging
import pymysql
import sys

from tbont_text_engine.utils import io
from tbont_text_engine.nlp import pipeline
from tbont_text_engine.vector_space import LSIModel


reload(sys)
sys.setdefaultencoding('utf-8')

# DATABASE INITIALIZATION

# db = pymysql.connect(host="azure.3bont.com",  # your host, usually localhost
#                      # your username
#                      user="ameniawy",
#                      # your password
#                      passwd="@3Bont.com",
#                      db="tresbon")  # name of the data base
# db.set_charset('utf8mb4')


db = pymysql.connect(host="localhost",  # your host, usually localhost
                     # your username
                     user="root",
                     # your password
                     passwd="root",
                     db="threebont")  # name of the data base
db.set_charset('utf8mb4')
# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s : %(levelname)s : %(message)s')

MIN_LENGTH = 5
MAX_LENGTH = 500


def update_entity(entity, entity_type):
    """
    Store entity into DB or update frequency if already exists.

    Args:
            entity(str): entity name.
            entity_tyoe(str): entity type.

    Retruns:
            None
    """

    word = entity

    cur.execute('SELECT count(id) FROM `ml_words` WHERE `word`=%s;', (word))
    oldRecord = cur.fetchone()

    if oldRecord[0] == 0:  # word does not already exist, so add it
        cur.execute(
            "INSERT INTO ml_words (word, entity_type, occurrence) VALUES(%s,%s,%s)", (word, entity_type, '1'))
    else:  # value is already there, update frequency
        cur.execute(
            'SELECT occurrence, id FROM `ml_words` WHERE `word`=%s;', (word))
        oldRecord = cur.fetchone()
        new_occurrence = int(oldRecord[0]) + 1

        cur.execute(
            "UPDATE ml_words SET occurrence=%s WHERE `word`=%s", (str(new_occurrence), word))

    db.commit()


def process_article(article, lang):
    """
        Calls the pipeline on the text and adds it to the DB.

        Args:
                article(str): article text.

        Returns: 

    """
    #try:
    tagged_text = pipeline.start_pipeline(article, language=lang)
    #except:
        #print article

    tokens = tagged_text.tokens
    entities = tagged_text.entities
    entities_list = []

    for entity in entities:
        entity_type = entities[entity]
        entities_list.append(entity)
        update_entity(str(entity), str(entity_type))

    # print "okk"

    return tokens, entities_list


def _get_article(rootdir, lang):
    """
        .

        Args:
                rootdir(str): path of root director.
                lang(str): language

        Returns: 
                list[list(str)]: list of list of strings.. articles represneted as tokens
    """
    all_ids = []
    all_tokens_dict = {}
    all_entities = []
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            path = os.path.join(subdir, file)
            file = open(path, 'r')
            text = ' '.join(file)


            ##################################################
            article_id = str(file).replace('.txt','').split('_')[1].split('\'')[0]
            #print article_id
            ##################################################

            length = len(text.split())
            if length < MIN_LENGTH or length > MAX_LENGTH:
                continue

            #try:
            tokens, entities = process_article(text, lang)
            # except Exception as e:
            # 	logging.error('Error processing article, skipped!')
            # 	continue
            all_entities = all_entities + entities
            all_tokens_dict[article_id] = tokens
            all_ids.append(article_id)

    return all_tokens_dict, all_entities, all_ids


def _add_vector_db(entity, vector):
    """
        Update the entity vector column.

        Args:
                entity(str): entity name.
                vector(numpy.ndarray: token vector)

        Returns: 
                None
    """
    vector_string = ''
    for vec in vector:
        vector_string = vector_string + str(vec) + ','

    # remove last char, unwanted comma
    vector_string = vector_string[:len(vector_string)-1]

    cur.execute(
        "UPDATE ml_words SET vector=%s WHERE `word`=%s", (vector_string, entity))


def _add_vector_article_db(article_id, vector):
    """
        Update the article vector column.

        Args:
                article_id(str): article id.
                vector(numpy.ndarray: token vector)

        Returns: 
                None
    """   
    vector_string = ''
    for vec in vector:
        vector_string = vector_string + str(vec) + ','

    # remove last char, unwanted comma
    vector_string = vector_string[:len(vector_string)-1]

    cur.execute(
        "UPDATE content SET vector=%s WHERE `id`=%s", (vector_string, article_id))    



#//////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////
# Start of English call
rootdir = 'datatry/en/'
logging.info('Grabbing English articles...')
all_tokens, all_entities, all_ids = _get_article(rootdir, 'en')


logging.info('Starting EN model..')
model_en = LSIModel()
logging.info('Training EN model with tokens..')
model_en.train_model(all_tokens)

# TODO: iterate over all_entities and get vector of each one then update DB

logging.info('Updating entities table with entity\'s vectors..')

# update entities with their vectors
for entity in all_entities:
    vector = model_en.get_token_vector(entity)
    _add_vector_db(entity, vector)

# update articles with their vectors
for article_id in all_ids:
    vector = model_en.get_article_vector(article_id)
    _add_vector_article_db(article_id, vector)

db.commit()

model_en.save('models/model_en.pkl')

#//////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////
# Start of Arabic call

rootdir2 = 'datatry/ar/'
logging.info('Grabbing Arabic articles...')
all_tokens, all_entities, all_ids = _get_article(rootdir2, 'ar')


logging.info('Starting AR model..')
model_ar = LSIModel()
logging.info('Training AR model with tokens..')
model_ar.train_model(all_tokens)


logging.info('Updating entities table with entity\'s vectors..')

# update entities with their vectors
for entity in all_entities:
    vector = model_ar.get_token_vector(entity)
    _add_vector_db(entity, vector)


# update articles with their vectors
for article_id in all_ids:
    vector = model_ar.get_article_vector(article_id)
    _add_vector_article_db(article_id, vector)


db.commit()

model_ar.save('models/model_ar.pkl')
