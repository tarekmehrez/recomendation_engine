#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from tbont_text_engine.nlp import entity_tagger


TEST_TEXT_EN = """

Manchester United assistant manager 'Rui Faria' says referee
Mark Clattenburg did "fantastic work" after sending Jose Mourinho
to the stands at half-time in the 0-0 draw with Burnley on Saturday.

"""

TEST_TAGS_EN = [(u'Manchester', u'I-ORG'),
                (u'United', u'I-ORG'),
                (u'assistant', u'O'),
                (u'manager', u'O'),
                (u"'", u'O'),
                (u'Rui', u'I-PER'),
                (u'Faria', u'I-PER'),
                (u"'", u'O'),
                (u'says', u'O'),
                (u'referee', u'O'),
                (u'Mark', u'I-PER'),
                (u'Clattenburg', u'I-PER'),
                (u'did', u'O'),
                (u'"', u'O'),
                (u'fantastic', u'O'),
                (u'work', u'O'),
                (u'"', u'O'),
                (u'after', u'O'),
                (u'sending', u'O'),
                (u'Jose', u'I-PER'),
                (u'Mourinho', u'I-PER'),
                (u'to', u'O'),
                (u'the', u'O'),
                (u'stands', u'O'),
                (u'at', u'O'),
                (u'half', u'O'),
                (u'-', u'O'),
                (u'time', u'O'),
                (u'in', u'O'),
                (u'the', u'O'),
                (u'0', u'O'),
                (u'-', u'O'),
                (u'0', u'O'),
                (u'draw', u'O'),
                (u'with', u'O'),
                (u'Burnley', u'I-ORG'),
                (u'on', u'O'),
                (u'Saturday', u'O'),
                (u'.', u'O')]


TEST_TEXT_AR = """
نجح روبيرت ليفاندوسكى فى إنهاء الصيام التهديفى الذى عانده فى
البوندزليجا بعد ستة مباريات دون هدف بتسجيل هدفين فى مرمى أوجسبورج
ليقود بايرن ميونيخ للإنتصار بثلاثة أهداف مقابل هدف. ليفاندوسكى.

"""

TEST_TAGS_AR = [(u'\u0646\u062c\u062d', u'O'),
                (u'\u0631\u0648\u0628\u064a\u0631\u062a', 'I-PER'),
                (u'\u0644\u064a\u0641\u0627\u0646\u062f\u0648\u0633\u0643\u0649', 'I-PER'),
                (u'\u0641\u0649', u'O'),
                (u'\u0625\u0646\u0647\u0627\u0621', u'O'),
                (u'\u0627\u0644\u0635\u064a\u0627\u0645', u'O'),
                (u'\u0627\u0644\u062a\u0647\u062f\u064a\u0641\u0649', u'O'),
                (u'\u0627\u0644\u0630\u0649', u'O'),
                (u'\u0639\u0627\u0646\u062f\u0647', u'O'),
                (u'\u0641\u0649', u'O'),
                (u'\u0627\u0644\u0628\u0648\u0646\u062f\u0632\u0644\u064a\u062c\u0627', u'O'),
                (u'\u0628\u0639\u062f', u'O'),
                (u'\u0633\u062a\u0629', u'O'),
                (u'\u0645\u0628\u0627\u0631\u064a\u0627\u062a', u'O'),
                (u'\u062f\u0648\u0646', u'O'),
                (u'\u0647\u062f\u0641', u'O'),
                (u'\u0628\u062a\u0633\u062c\u064a\u0644', u'O'),
                (u'\u0647\u062f\u0641\u064a\u0646', u'O'),
                (u'\u0641\u0649', u'O'),
                (u'\u0645\u0631\u0645\u0649', u'O'),
                (u'\u0623\u0648\u062c\u0633\u0628\u0648\u0631\u062c', u'O'),
                (u'\u0644\u064a\u0642\u0648\u062f', u'O'),
                (u'\u0628\u0627\u064a\u0631\u0646', 'I-ORG'),
                (u'\u0645\u064a\u0648\u0646\u064a\u062e', 'I-ORG'),
                (u'\u0644\u0644\u0625\u0646\u062a\u0635\u0627\u0631', u'O'),
                (u'\u0628\u062b\u0644\u0627\u062b\u0629', u'O'),
                (u'\u0623\u0647\u062f\u0627\u0641', u'O'),
                (u'\u0645\u0642\u0627\u0628\u0644', u'O'),
                (u'\u0647\u062f\u0641', u'O'),
                (u'.', u'O'),
                (u'\u0644\u064a\u0641\u0627\u0646\u062f\u0648\u0633\u0643\u0649', 'I-PER'),
                (u'.', u'O')]


class TestEntityTagger(unittest.TestCase):

    def test_ner_en(self):
        output = entity_tagger.extract_entities(TEST_TEXT_EN, language='en')
        self.assertListEqual(output, TEST_TAGS_EN, msg=None)

    def test_ner_ar(self):
        output = entity_tagger.extract_entities(TEST_TEXT_AR, language='ar')
        self.assertListEqual(output, TEST_TAGS_AR, msg=None)
