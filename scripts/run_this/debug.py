# Author : Abdelrahman

import os
import logging

from tbont_text_engine.vector_space import LSIModel
from tbont_text_engine.nlp import pipeline


logging.basicConfig(
	level=logging.DEBUG,
	format='%(asctime)s : %(levelname)s : %(message)s')

en_path = os.path.realpath('models/model_en.pkl')
rootdir = 'data'

all_tokens_dict = {}

for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		path = os.path.join(subdir, file)
		file = open(path, 'r')
		text = ' '.join(file)

		length = len(text.split())
		if length < 5 or length > 500:
			continue

		tagged_text = pipeline.start_pipeline(text, language='en')
		tokens = tagged_text.tokens


		##################################################
		article_id = str(file).replace('.txt','').split('_')[1].split('\'')[0]
		##################################################



		all_tokens_dict[article_id] = tokens



logging.info('Loading model_en.pkl')
model_en = LSIModel()
model_en.load(en_path)

model_en.update_model(all_tokens_dict)
