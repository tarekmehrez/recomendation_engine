"""Contains the entity tagging module."""
from polyglot.text import Text as PolyglotExtractor


def extract_entities(text, language):
    """
    Extract tags (entities) for a given text.

    params:
        text (str)
    returns:
        list[tuple(str)] each token and it's tag
    """
    tagged_text = PolyglotExtractor(text, hint_language_code=language)
    entities = tagged_text.entities

    # extracting entities and their tags
    entities_dict = {}
    for entity in entities:
        for token in entity:
            entities_dict[token] = entity.tag

    # writing output in stanford format
    formatted_output = []
    for token in tagged_text.words:
        if token in entities_dict.keys():
            formatted_output.append((token, entities_dict[token]))
        else:
            formatted_output.append((token, u'O'))

    return formatted_output
