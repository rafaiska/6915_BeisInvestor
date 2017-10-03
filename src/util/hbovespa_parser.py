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
        fileContent = open('data/cotacões.txt', 'r')

        cotacoes = open("data/cotacoesOrganizadas.json", 'w')
        listBovespa = [{}]

        for phraseLine in iter(fileContent):
            flagAux = 0
            date = ""
            companyName = ""
            valor = ""
            for char in range(2, 230):
                if(char == 5 or char == 7):
                    date = date + phraseLine[char] + "/"
                elif(char <= 9 and (char != 5 or char !=7)):
                    date = date + phraseLine[char]
                elif(27 <= char <= 35):
                    if(phraseLine[char] == " " or flagAux == 1):
                        if(flagAux == 0):
                            flagAux = 1
                        continue
                    companyName = companyName + phraseLine[char]
                elif(56 <= char <= 230):
                    valor = valor + phraseLine[char]
            listBovespa.append({'Empresa': companyName, 'Data': date, 'Valor': valor})
        print(listBovespa)
        print('PARSING FILE INTO JSON...')
        json.dump(listBovespa, cotacoes)
        cotacoes.close()
        print('OUTPUT FILE WRITTEN TO %s' % (self.outputfile))

    def check_json(self):
        """Checks if file already exists"""
        if os.path.isfile(self.outputfile):
            return True
        else:
            return False
