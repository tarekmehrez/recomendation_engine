"""Contains io module."""

import os
import cPickle

from gensim.models import Doc2Vec

from tbont_text_engine.exceptions import FormatNotSupportedError

SUPPORTED_READ_EXTENSIONS = ['.txt', '.pkl', '.w2v']
SUPPORTED_WRITE_EXTENSIONS = ['.pkl', '.w2v']


def exists(file_path):
    """
    Check if path exists.

    params:
        file_path (str): path to the file to be checked
    Returns:
        bool: whether it exists or not
    """
    return os.path.exists(file_path)


def read(file_path):
    """
    Check extension, calls respective read function.

    params:
        file_path (str): path to the file to be read
    """
    _, extension = os.path.splitext(file_path)

    if extension not in SUPPORTED_READ_EXTENSIONS:
        raise FormatNotSupportedError(
            'Cant read file with %s format' % extension)

    if extension == '.txt':
        return _read_txt(file_path)

    elif extension == '.pkl':
        return _read_pkl(file_path)

    elif extension == '.w2v':
        return _read_word2vec_model(file_path)


def _read_txt(file_path):
    """
    Read txt files.

    params:
        file_path (str): path to the file to be read
    returns:
        str: content of the txt file
    """
    with open(file_path) as f:
        content = f.read()

    return content


def _read_pkl(file_path):
    """
    Read pkl files.

    params:
        file_path (str): path to the file to be read
    returns:
        obj: content of the pkl file
    """
    with open(file_path, 'rb') as f:
        content = cPickle.load(f)

    return content


def _read_word2vec_model(file_path):
    """
    Save word2vec gensim model.

    params:
        file_path (str): path to the output file
    returns:
        gensim.models.Doc2Vec
    """
    return Doc2Vec.load(file_path)


def write(content, file_path):
    """
    Check extension, calls respective write function.

    Args:
        content (obj): content of the file to be written
        file_path (str): path to the output file
    """
    _, extension = os.path.splitext(file_path)
    if extension not in SUPPORTED_WRITE_EXTENSIONS:
        raise FormatNotSupportedError(
            'Cant write file with %s format' % extension)

    if extension == '.pkl':
        _write_pkl(content, file_path)

    elif extension == '.w2v':
        _write_word2vec_model(content, file_path)


def _write_pkl(content, file_path):
    """
    Write content to a pkl format.

    params:
        content (obj): content of the file to be written
        file_path (str): path to the output file
    """
    with open(file_path, 'wb') as f:
        cPickle.dump(content, f, 2)


def _write_word2vec_model(model, file_path):
    """
    Save word2vec gensim model.

    params:
        model (gensim.models.Doc2Vec)
        file_path (str): path to the output file
    """
    model.save(file_path)
