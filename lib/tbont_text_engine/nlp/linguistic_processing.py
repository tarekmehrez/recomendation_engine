"""
Contains NLP helper functions.

functions take a list of tuples
each tuple is a token and its tag (entity representation)
tagged_tokens are filtered throughout this module's functions
The surviving tagged_tokens are then returned alongside their tags

"""
from stop_words import get_stop_words
from nltk.corpus import stopwords as nltk_stop_words

# prepare stop words lists for en and ar
EN_STOP_WORDS = nltk_stop_words.words('english')
EN_STOP_WORDS += get_stop_words('en')
EN_STOP_WORDS = list(set(EN_STOP_WORDS))

AR_STOP_WORDS = get_stop_words('ar')

STOP_WORDS = {}
STOP_WORDS['en'] = EN_STOP_WORDS
STOP_WORDS['ar'] = AR_STOP_WORDS


def process_tokens(tagged_tokens, language):
    """
    Process list of tagged_tokens.

    params:
        tagged_tokens list[str]
        language (str)
    returns:
        list(str): processed tagged_tokens
    """
    tagged_tokens = _strip_punctuation(tagged_tokens)
    tagged_tokens = _lower_case(tagged_tokens)
    tagged_tokens = _strip_stop_words(tagged_tokens, language)

    return tagged_tokens


def _strip_punctuation(tagged_tokens):
    """
    Remove punctiation.

    Exceptions are:
    '_' for entities (i.e manchester_united)
    '-' for match scores

    params:
        tagged_tokens (list[tuple(str,str)])
    Returns
       list[tuple(str,str)]: tagged_tokens without puncts.
    """
    return [(token, tag)
            for token, tag in tagged_tokens
            if token.isalnum() or '-' in token or '_' in token]


def _lower_case(tagged_tokens):
    """
    Lowercase.

    params:
        tagged_tokens (list[tuple(str,str)])
    Returns
       list[tuple(str,str)]: lowercased tagged_tokens.
    """
    return [(token.lower(), tag)
            for (token, tag) in tagged_tokens]


def _strip_stop_words(tagged_tokens, language):
    """
    Remove stop words.

    params:
        tagged_tokens (list[tuple(str,str)]): tokenized words
        language (str)
    returns:
        list[tuple(str,str)]: tagged_tokens with stop words dropped
    """
    return [(token, tag)
            for token, tag in tagged_tokens
            if token not in STOP_WORDS[language]]
