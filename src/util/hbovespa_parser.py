import json
import os


class HBovespaParser(object):
    """Parses Bovespa history file (gziped) into a json structured file"""
    def __init__(self, gzpath='data/cotacoes.gz', outputfile='data/cotacoes.json'):
        self.gzpath = gzpath
        self.outputfile = outputfile

    def parse(self):
        """Parses file"""
        print('DECOMPRESSING FILE: %s...' % (self.gzpath))
        # TODO: descompactar o arquivo

        print('PARSING FILE INTO JSON...')
        # TODO: converter o arquivo para formato json

        print('OUTPUT FILE WRITTEN TO %s' % (self.outputfile))

    def check_json(self):
        """Checks if file already exists"""
        if os.path.isfile(self.outputfile):
            return True
        else:
            return False
