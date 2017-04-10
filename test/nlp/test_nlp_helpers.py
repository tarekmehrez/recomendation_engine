#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
from collections import namedtuple

from tbont_text_engine.nlp import nlp_helpers

TestCase = namedtuple('TestCase', ['input', 'expected'])


class TestNLPHelpers(unittest.TestCase):

    def test_lower_case(self):
        test_cases = [TestCase(input='testing ALL CAPS',
                               expected='testing all caps'),
                      TestCase(input='testing no caps',
                               expected='testing no caps')]
        for case in test_cases:
            output = nlp_helpers._lower_case(case.input.split())
            self.assertEqual(output, case.expected.split())

    def test_strip_stop_words(self):
        test_cases = [TestCase(input='test be is there the a word',
                               expected='test word'),
                      TestCase(input='they re testing again stop words',
                               expected='testing stop words')]
        for case in test_cases:
            output = nlp_helpers._strip_stop_words(case.input.split(),
                                                   language='en')
            self.assertEqual(output, case.expected.split())

    def test_strip_punctuation(self):
        test_cases = [TestCase(input='test , with - some . Puncts !',
                               expected='test with some Puncts'),
                      TestCase(input='test no puncts',
                               expected='test no puncts')]

        for case in test_cases:
            output = nlp_helpers._strip_punctuation(case.input.split())
            self.assertEqual(output, case.expected.split())
