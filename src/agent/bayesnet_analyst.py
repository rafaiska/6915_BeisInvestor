import datetime
import json
from operator import itemgetter

import src.agent.bayesnet_constructor as constructor
import src.agent.findbest as findbest

class BayesAnalyst(object):
    def __init__(self):
        pass

    def analyze_data(self, filename):
        best_to_invest = None
        starttime = datetime.datetime.now()

        print('BEGINNING ANALYSIS AT %s...' % (datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')))

        try:
            with open(filename, 'r') as fpointer:
                datajson = json.load(fpointer)
                fpointer.close()
        except IOError:
            print('ERROR: CANNOT LOAD PARSED JSON')
            return None
        except ValueError:
            print('ERROR: BAD FORMAT FOR DATA JSON')
            return None

        print('GENERATING BAYES NET...')
        bnet, companies = constructor.generate_bayesnet(sorted(datajson, key=itemgetter('Data')))
        print('DONE!')
        print('EVALUATING RECENT STOCK BEHAVIOR...')
        best_to_invest = findbest.findbest(bnet, 'data/entrada.json', companies)

        print('ANALYSIS COMPLETED')
        elapsed_time = datetime.datetime.now() - starttime
        print('ELAPSED TIME: %d days, %d hours, %d minutes, %d seconds' %
              (elapsed_time.days,
               (elapsed_time.seconds - (elapsed_time.seconds % 3600)) / 3600,
               (elapsed_time.seconds - elapsed_time.seconds % 60) / 60,
               elapsed_time.seconds % 60))
        return best_to_invest