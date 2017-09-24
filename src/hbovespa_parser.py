import json
import os


class HBovespaParser(object):
    """Parses Bovespa history file (gziped) into a json structured file"""
    def __init__(self, gzpath='data/cotacoes.gz', outputfile='data/cotacoes.json'):
        self.gzpath = gzpath
        self.outputfile = outputfile

    def parse(self):
        """Parses file"""
        pass

    def check_json(self):
        """Checks if file was created"""
        pass
