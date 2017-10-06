import json
import os
import gzip


class HBovespaParser(object):
    """Parses Bovespa history file (gziped) into a json structured file"""
    def __init__(self, gzpath='data/cotacoes.gz', outputfile='data/cotacoes.json'):
        self.gzpath = gzpath
        self.outputfile = outputfile

    def parse(self):
        """Parses file"""
        print('DECOMPRESSING FILE: %s...' % (self.gzpath))
        # TODO: descompactar o arquivo
        fileGz = gzip.open(self.gzpath, 'rb')
        fileContent = open('data/cotacões.txt', 'wb')
        fileContent.write(fileGz.read())
        fileGz.close()
        fileContent.close()
        fileContent = open('data/cotacoes.txt', 'r')

        cotacoes = open("data/cotacoes.json", 'w')
        listaBovespa = []

        print ('PARSING FILE TO JSON...')
        for line in iter(fileContent):
            date = self.getDate(line)
            name = self.getCompanyName(line)
            value = self.getClosingValue(line)

            print (date, name, value)
            listaBovespa.append({
                'Empresa': name,
                'Data': date,
                'Valor': value,
            })

        json.dump(listaBovespa, cotacoes)
        cotacoes.close()
        print('OUTPUT FILE WRITTEN TO %s' % (self.outputfile))

    def check_json(self):
        """Checks if file already exists"""
        if os.path.isfile(self.outputfile):
            return True
        else:
            return False

    def getDate(self, line):
        '''Returns the date from a line (starts at pos 2, ends at pos 9)'''
        year = line[2] + line[3] + line[4] + line[5]
        month = line[6] + line[7]
        day = line[8] + line[9]

        date = day + '/' + month + '/' + year
        return date

    def getCompanyName(self, line):
        '''Returns the company name from a line (starts at pos 27, ends when whitespace is found)'''
        name = ""
        index = 27
        while not line[index].isspace():
            name = name + line[index]
            index = index + 1
        return name

    def getClosingValue(self, line):
        '''Returns the closing value from a line, format is xx,xx (starts at pos 136, ends at pos 149)'''
        value = ""
        index = 136
        while line[index] == "0":
            index = index + 1
            # Case of missing values from BOVESPA data
            if (index == 149):
                return "00,00"

        while index != 147:
            value = value + line[index]
            index = index + 1
        value = value + ',' + line[148] + line[149]
        return value

