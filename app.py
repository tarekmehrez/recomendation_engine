"""Contains the rec engine online api."""
import json

from flask import Flask
from flask import request

from tbont_text_engine.vector_space import arithmetic

app = Flask(__name__)


@app.route("/")
def index():
    """
    Index testing.
    """
    return "What are you looking for, mate?"


@app.route("/get_closest")
def get_closest_api():
    """
    Flask endpoint that calls arithmetic.get_closest.

    returns:
        see tbont_text_engine.vector_space.arithmetic::get_closest
    """
    args = json.loads(request.get_json())
    vector = args['vector']
    vectors_dict = args['vectors_dict']
    num_results = arithmetic.get_closest.func_defaults[0]

    if 'num_results' in args:
        num_results = args['num_results']

    result = arithmetic.get_closest(vector, vectors_dict, num_results)
    return json.dumps({'result': result})


@app.route("/get_average")
def get_average():
    """
    Flask endpoint that calls arithmetic.get_average.

    returns:
        see tbont_text_engine.vector_space.arithmetic::average_vectors
    """
    args = json.loads(request.get_json())
    vector = args['vector']
    result = arithmetic.average_vectors(vector)
    return json.dumps({'result': result})
