# Abdelrahman

import os
import math
import sys
import logging

from collections import defaultdict

reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(
            level=logging.DEBUG,
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


def _get_tfidf(articles, tf, df):
    """
        Calculates tfidf matrix.

        Args:
                articles(list): list of articles.
                tf(list(dict)): dict of term frequency.
                df(dict): dict of docs containing word.
        
        Returns:
                list(dict): list of dicts(vector) containing tfidf values
    """
    articles_tfidf = []
    length = len(articles)

    for i in range(length):
    	entry = articles[i]
    	term_freq = tf[i]
    	tfidf_dict = defaultdict(float)
    	for word in term_freq:
    		tfidf = term_freq[word] * (math.log(number_of_docs)/df[word])
    		tfidf_dict[word] = tfidf

    	articles_tfidf.append(tfidf_dict)

    return articles_tfidf

#////////////////////////////////////////////////////
rootdir = 'data/en/'
logging.info('Grabbing articles...')
articles = _get_article(rootdir)

frequencies = defaultdict(int)
df = defaultdict(int)
number_of_docs = len(articles)
tf = []

logging.info('Started processing...')
for entry in articles:
    df_local = defaultdict(int)

    for token in entry.split(' '):
        frequencies[token] += 1
        # check for df
        df_local[token] = 1

    for word in df_local:
        df[word] += 1

    # count tf
    tf_local = defaultdict(int) #term frequency of this specific article 
    for word in entry.split(' '):
        tf_local[word] += 1
    tf.append(tf_local)


logging.info('Generating TF IDF...')
articles_tfidf = _get_tfidf(articles, tf, df)



logging.info('Printing...')
# Just printing 1 dict as a test
x = 0
for tf in articles_tfidf:
    if x > 50 and x < 60:
        for value in tf:
            print value + ' TFIDF: ' + str(tf[value])
        print "----------------------------------------------"
    x += 1


# print df


# df current entry then update global df list


# read files, each file as an entry in a list

# create a set of vocab, unique  words in all docs DONE

# count words, how many times did token t occurr in all docs DONE

# create tf-idf matrix


# for each term,doc pair
# how many times did term t occurr in doc d
# how many docs contain term t
# calculate tfi-df
