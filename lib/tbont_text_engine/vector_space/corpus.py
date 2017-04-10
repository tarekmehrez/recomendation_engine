"""
Contains the corpus class.

. Build dictionary: tokens2ids, ids2tokens
. Transrom
"""
from gensim import corpora, models

# TODO: online streaming of articles instead of laoding all into memory
# example: http://tinyurl.com/jpt38at


class Corpus(object):

    """Build Corpus instance using gensim's corpus module."""

    def __init__(self):
        """Init Corpus instance."""
        self.tfidf_matrix = None
        self.dictionary = None

    def build(self, articles_as_tokens):
        """
        Build a gensim corpus from tokenized articles.

        Corpus = bow/tfidf sparse matrix

        params:
            articles_as_tokens (list[list(str)])
        """
        self.dictionary = _create_dictionary(articles_as_tokens)
        corpus = _corpus_to_bow(self.dictionary, articles_as_tokens)
        self.tfidf_matrix = _bow_to_tfidf(corpus)

    def merge(self, articles_as_tokens):
        """
        Add new documents to the corpus.

        params:
            articles_as_tokens (list[list(str)])
        """
        self.dictionary = _add_to_dictionary(
            self.dictionary, articles_as_tokens)
        new_corpus = _corpus_to_bow(self.dictionary, articles_as_tokens)
        new_tfidf_matrix = _bow_to_tfidf(new_corpus)

        self.tfidf_matrix += new_tfidf_matrix

        # new documents to be added to the model
        return new_tfidf_matrix


def _create_dictionary(articles_as_tokens):
    """
    Create gensim Dictionary.

    params:
        articles_as_tokens (list[list(str)])
    returns:
        dictionary (gensim.corpora.Dictionary)
    """
    return corpora.Dictionary(articles_as_tokens)


def _add_to_dictionary(dictionary, articles_as_tokens):
    """
    Update gensim Dictionary.

    params:
        dictionary (gensim.corpora.Dictionary)
        articles_as_tokens (list[list(str)])
    returns:
        dictionary (gensim.corpora.Dictionary)
    """
    dictionary.add_documents(articles_as_tokens)
    return dictionary


def _corpus_to_bow(dictionary, articles_as_tokens):
    """
    Create bow representation.

    params:
        articles_as_tokens (list[list(str)])
    returns:
        list[list(tuple(int,int))]
    """
    return [dictionary.doc2bow(article) for article in articles_as_tokens]


def _bow_to_tfidf(corpus):
    """
    Transform corpus to tfidf space.

    params:
        corpus (list[list(tuple(int,int))])
    returns:
        list[list(tuple(int, int))]: tfidf matrix
    """
    tfidf_transofmer = models.TfidfModel(corpus)
    return [tfidf_transofmer[article] for article in corpus]
