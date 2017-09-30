import datetime

class BayesAnalyst(object):
    def __init__(self):
        pass

    def analyze_data(self, filename):
        best_to_invest = None
        starttime = datetime.datetime.now()

        print('BEGINNING ANALYSIS AT %s...' % (datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')))

        # TODO: Fazer analise dos dados em json

        print('ANALYSIS COMPLETED')
        elapsed_time = datetime.datetime.now() - starttime
        print('ELAPSED TIME: %d days, %d hours, %d minutes, %d seconds' %
              (elapsed_time.days,
               (elapsed_time.seconds - (elapsed_time.seconds % 3600)) / 3600,
               (elapsed_time.seconds - elapsed_time.seconds % 60) / 60,
               elapsed_time.seconds % 60))
        return best_to_invest