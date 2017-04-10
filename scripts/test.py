"""
A test script that reads 50K articles per language for training,
and updates the model on another 10k
"""
import os
import logging

from tbont_text_engine.nlp import pipeline
from tbont_text_engine.utils import io
from tbont_text_engine.vector_space import LSIModel


logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)


def read_content(files, lang):
    articles = []
    for idx, en_file in enumerate(files):
        print '[*][*] reading file %i' % idx
        content = io.read(en_file)
        tagged_text = pipeline.start_pipeline(content, lang)
        tokens = tagged_text.tokens
        articles.append(tokens)

    return articles


def get_file_names(file):

    with open(file) as f:
        file_names = f.read().split('\n')
    return filter(None, file_names)


os.chdir('../data')


print '[*] reading file names...'

en_files = get_file_names('en.txt')

print '[*] reading training content for en and ar...'

en_train_articles = dict(
    zip(range(1000), read_content(en_files[:1000], 'en')))

print '[*] reading update content for en and ar...'

en_update_articles = dict(
    zip(range(1000, 1500), read_content(en_files[1000:1500], 'en')))


en_model = LSIModel()

print '[*] training en model...'
en_model.train_model(en_train_articles)

print '[*] updating en model...'
en_model.update_model(en_update_articles)


print '########## DONE ############'
