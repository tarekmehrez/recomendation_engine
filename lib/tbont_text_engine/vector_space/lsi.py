"""Contains the LSIModel class."""
from collections import OrderedDict

from gensim import models, matutils

from corpus import Corpus
from tbont_text_engine.utils import io


class LSIModel(object):

    """Train LSIModel using gensim's API."""

    def __init__(self):
        """Init LSIModel instance."""
        self.model = None
        self.corpus = Corpus()
        self.token_vectors = []
        self.articles_vectors = []
        self.article_to_idx = OrderedDict()

    def train_model(self, articles_as_tokens, num_topics=100):
        """
        Train LSI Model.

        params:
            num_topics (int) [default=100]
        """
        self.corpus.build(articles_as_tokens.values())
        self._assign_article_ids(articles_as_tokens.keys())

        self.model = models.LsiModel(corpus=self.corpus.tfidf_matrix,
                                     num_topics=num_topics)
        self._extract_matrices()

    def _assign_article_ids(self, articles_ids):
        """
        Assign article ids.

        params:
            articles_ids (list[str])
        """
        indices = range(len(articles_ids))
        self.article_to_idx = dict(zip(articles_ids, indices))

    def update_model(self, articles_as_tokens):
        """
        Add new documents to the LSI vector space.

        params:
            articles_as_tokens (dict{str: list[list(str)]}): article id, tokens
        """
        print 'updating...'
        print 'merging corpus...'
        new_documents = self.corpus.merge(articles_as_tokens.values())

        print 'updating ids...'
        self._update_article_ids(articles_as_tokens.keys())

        print 'adding new documents...'
        self.model.add_documents(new_documents)

        print 'extracting new matrix'
        self._extract_matrices()

    def _update_article_ids(self, articles_ids):
        """
        Update article ids.

        params:
            articles_ids (list[str])
        """
        max_so_far = max(self.article_to_idx.values())
        new_max = max_so_far + len(articles_ids)
        new_indices = range(max_so_far + 1, new_max + 1)
        self.article_to_idx.update(dict(zip(new_indices, articles_ids)))

    def _extract_matrices(self):
        """
        Extract U, V matrices from LSI model.

        U: num_topics * num_tokens
        V: num_docs * num_topics

        So basically U is the tokens aginst topics vector
        V is the articles against topics vector
        http://tinyurl.com/hzxm4ty
        *** requires background on how LSI works ***
        """
        self.token_vectors = self.model.projection.u
        self.articles_vectors = matutils.corpus2dense(
            self.model[self.corpus.tfidf_matrix],
            len(self.model.projection.s)).T / self.model.projection.s

    def get_article_vector(self, article_id):
        """
        Get article vector.

        params:
            article_id (str)
        returns:
            numpy.ndarray: article vector
        """
        article_idx = self.article_to_idx[article_id]
        return self.articles_vectors[article_idx]

    def get_token_vector(self, token):
        """
        Get token vector.

        params:
            token (str)
        return:
            numpy.ndarray: token vector
        """
        token_id = self.corpus.dictionary.token2id[token]
        return self.token_vectors[token_id]

    def load(self, file_path):
        """
        Load entire LSIModel instance.

        params:
            file_path (str)
        """
        content = io.read(file_path)
        self.__dict__.update(content)

    def save(self, file_path):
        """
        Save entire LSIModel instance.

        params:
            file_path (str)
        """
        content = self.__dict__
        io.write(content, file_path)
