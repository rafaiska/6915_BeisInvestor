import json
from operator import itemgetter

from .bayesnet_constructor import get_variation

def findbest(bayesnet, inputpath, companies_names):
    with open(inputpath, 'r') as inputfile:
        inputjson = json.load(inputfile)

    inputjson = sorted(inputjson, key=itemgetter('Data'))
    previous_day = inputjson[0]['Data']
    today = inputjson[len(inputjson) -1]['Data']

    today_prices = {}
    previous_day_prices = {}
    for entry in inputjson:
        if entry['Data'] == today:
            today_prices[entry['Empresa']] = entry['Valor']
        elif entry['Data'] == previous_day:
            previous_day_prices[entry['Empresa']] = entry['Valor']
        else:
            print('ERROR: INVALID INPUT FILE')
            return None

    variation = get_variation(today_prices, previous_day_prices, companies_names)
    pattern = ''
    for company_name in companies_names:
        pattern += variation[company_name]

    choice_weight = []
    for company_name in companies_names:
        try:
            u_chance = bayesnet[company_name][pattern]['u']
            s_chance = bayesnet[company_name][pattern]['s']
            d_chance = bayesnet[company_name][pattern]['d']
        except KeyError:
            print('INSUFFICIENT DATA FOR ANALYSIS')
            return None
        weight = u_chance * 2.0
        weight += s_chance * 1.0
        weight += d_chance * (- 1.0)
        choice_weight.append({'company': company_name, 'weight': weight,
                              'u_chance': u_chance, 's_chance': s_chance, 'd_chance': d_chance})

    choice_weight = sorted(choice_weight, key=itemgetter('weight'), reverse=True)
    return choice_weight[0]
