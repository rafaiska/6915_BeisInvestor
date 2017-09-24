from src.hbovespa_parser import HBovespaParser

import unittest
import json


class TestHBovespaParser(unittest.TestCase):
    def setUp(self):
        self.parser = HBovespaParser()

    def test_parse(self):
        self.parser.parse()
        with open('data/cotacoes.json', 'r') as jsonfile:
            jsondata = json.load(jsonfile)
        self.assertEqual(jsondata['intel']['20160402'], '4,332141')
        self.assertEqual(jsondata['intel']['20160402'], '4,332141')
        self.assertEqual(jsondata['intel']['20160402'], '4,332141')
        self.assertEqual(jsondata['intel']['20160402'], '4,332141')
        self.assertEqual(jsondata['intel']['20160402'], '4,332141')

    def test_checkfile(self):
        self.assertEqual(self.parser.check_json(), True)
