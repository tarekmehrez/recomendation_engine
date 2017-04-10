"""Contains similarity functions."""
import operator
from collections import OrderedDict

import numpy as np
from scipy.spatial.distance import cosine


def get_closest(vector, vectors_dict, num_results=5):
    """
    Get the closest N vectors to vector.

    params:
        vector (numpy.ndarray)
        vectors_list (dict{str:numpy.ndarray}: ids and vectors
        num_results (int) [default=5]
    returns:
        dict{str: numpy.ndarray} closest N vectors and their ids as keys
    """
    similarity_scores = {}

    for current_vector_id, current_vector in vectors_dict.iteritems():
        current_score = cosine(vector, current_vector)
        similarity_scores[current_vector_id] = current_score

    # sort according to scores ~ rank search results
    sorted_scores = sorted(similarity_scores.items(),
                           key=operator.itemgetter(1))

    return OrderedDict(sorted_scores).keys()


def average_vectors(vectors):
    """
    Get average of vectors.

        vectors (list[list[float]])

    return:
        list[float]
    """
    return np.mean(vectors, axis=0).tolist()
