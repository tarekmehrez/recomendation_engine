"""Contains the nlp pipeline."""
from collections import namedtuple

import tagger
import linguistic_processing
from tbont_text_engine.exceptions import LanguageNotSupportedError
from tbont_text_engine.exceptions import IllegalArgumentError

ProcessedText = namedtuple('ProcessedText', ['tokens', 'entities'])
SUPPORTED_LANGUAGES = ['en', 'ar']


def start_pipeline(article, language):
    """
    Start the nlp pipeline to tag and tokenize text.

    params:
        article (str)
        language (str)
    returns:
        list[str]: list of tokens
        dict{str:str}: tokens that are entities and their types
    """
    if language not in SUPPORTED_LANGUAGES:
        raise LanguageNotSupportedError(
            '%s is not supported yet, currently supported languages are %s' %
            (language, SUPPORTED_LANGUAGES))

    if not (isinstance(article, str) or isinstance(article, unicode)):
        raise IllegalArgumentError('Expcected article as a string')

    tagged_tokens = tagger.extract_entities(article, language)
    merged_tokens = _merge_entities(tagged_tokens)
    cleaned_tokens = linguistic_processing.process_tokens(merged_tokens,
                                                          language)

    if len(cleaned_tokens) == 0:
        return ProcessedText([], {})

    entities = _collect_entities(cleaned_tokens)

    return ProcessedText(tokens=zip(*cleaned_tokens)[0],
                         entities=entities)


def _merge_entities(tagged_tokens):
    """
    Merge entities to a single token with underscore.

    Example:
    ('Manchester', 'I-ORG'),
    ('United'), 'I-ORG'),
    to ('Manchester_United', 'I-ORG')

    params:
        tagged_tokens list[tuple(str,str)]: tokens and their tags
    returns:
        list[tuple(str,str)]: merged tokens and their tags
    """
    # TODO: Clean this function!
    tokens = []

    current_entity = ''
    last_type = ''
    for token, entity_type in tagged_tokens:
        if entity_type != 'O':
            if current_entity == '':
                current_entity = token
            else:
                current_entity += '_' + token
            last_type = entity_type
        else:
            if current_entity == '':
                tokens.append((token, 'O'))
            else:
                tokens.append((current_entity, last_type))
                current_entity = ''

    return tokens


def _collect_entities(cleaned_tokens):
    """
    Collect entities in a separate dict.

    params:
        cleaned_tokens list[tuple(str,str)]
    returns:
        dict{str, str}: token as key, entity type as value
    """
    entities = {}
    for token, tag in cleaned_tokens:
        if tag != 'O':
            entities[token] = tag

    return entities
