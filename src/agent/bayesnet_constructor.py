from queue import Queue
from queue import Empty

STOCK_PRICE_VAR = 2.0


def fetch_companies_names(hist_json):
    names = set()
    for entry in hist_json:
        names.add(entry['Empresa'])
    names = sorted(names)
    print('STOCKS FOUND:', names)
    return names


def get_variation(today, previous, companies):
    """Tells whether companies stock prices have gone up (u), down (d), stayed the same (s) or there were not
    enough data available to compute variation (n)"""
    if previous is None:
        return None

    variation = {}
    for company_name in companies:
        if (company_name not in previous or
                    company_name not in today or
                    previous[company_name] is None or
                    today[company_name] is None):
            variation[company_name] = 'n'
            continue
        if previous[company_name] == 0.0:
            if today[company_name] > 0.0:
                variation[company_name] = 'u'
            else:
                variation[company_name] = 's'
        else:
            percentual_variation = (today[company_name] - previous[company_name]) / previous[company_name]
            percentual_variation *= 100.0

            if percentual_variation > STOCK_PRICE_VAR:
                variation[company_name] = 'u'
            elif percentual_variation < - STOCK_PRICE_VAR:
                variation[company_name] = 'd'
            else:
                variation[company_name] = 's'

    return variation


def generate_patternmap(blists, companies):
    patternmap = {}
    length = None
    for company_name in companies:
        patternmap[company_name] = {}
        if length is None or len(blists[company_name]) < length:
            length = len(blists[company_name])

    for i in range(length - 1):
        pattern_string = ''
        for company_name in blists:
            pattern_string += blists[company_name][i]
        for company_name in blists:
            if blists[company_name][i + 1] == 'n':
                continue
            if pattern_string not in patternmap[company_name].keys():
                patternmap[company_name][pattern_string] = []
            patternmap[company_name][pattern_string].append(blists[company_name][i + 1])
    return patternmap


def normalize_patternmap(pattern_map):
    new_pattern_map = {}
    for company_name in pattern_map:
        new_pattern_map[company_name] = {}
        for pattern in pattern_map[company_name]:
            if pattern.find('n') != -1:
                result = pattern_map[company_name][pattern]
                new_patterns = []
                patterns_to_process = Queue()
                current_pattern = pattern
                while current_pattern is not None:
                    npos = current_pattern.find('n')
                    if npos == -1:
                        new_patterns.append(current_pattern)
                    else:
                        for substitute in ['u', 's', 'd']:
                            newpattern = list(current_pattern)
                            newpattern[npos] = substitute
                            newpattern = ''.join(newpattern)
                            patterns_to_process.put_nowait(newpattern)
                    try:
                        current_pattern = patterns_to_process.get_nowait()
                    except Empty:
                        current_pattern = None

                for new_pattern in new_patterns:
                    if new_pattern not in new_pattern_map[company_name].keys():
                        new_pattern_map[company_name][new_pattern] = []
                    new_pattern_map[company_name][new_pattern].extend(result)
            else:
                if pattern in new_pattern_map[company_name].keys():
                    new_pattern_map[company_name][pattern].extend(pattern_map[company_name][pattern])
                else:
                    new_pattern_map[company_name][pattern] = [].extend(pattern_map[company_name][pattern])

    return new_pattern_map


def compute_patterns(pattern_map):
    bayesnet = {}

    for company_name in pattern_map:
        bayesnet[company_name] = {}
        for pattern in pattern_map[company_name]:
            length = len(pattern_map[company_name][pattern])
            if length <= 0:
                continue
            bayesnet[company_name][pattern] = {}
            bayesnet[company_name][pattern]['u'] = float(pattern_map[company_name][pattern].count('u')) / float(length)
            bayesnet[company_name][pattern]['s'] = float(pattern_map[company_name][pattern].count('s')) / float(length)
            bayesnet[company_name][pattern]['d'] = float(pattern_map[company_name][pattern].count('d')) / float(length)
    return bayesnet


def generate_bayesnet(hist_json):
    companies_names = fetch_companies_names(hist_json)
    behavior_list = {}

    for company_name in companies_names:
        behavior_list[company_name] = []

    current_date = hist_json[0]['Data']
    today_prices = {}
    previous_day_prices = {}
    for entry in hist_json:
        if entry['Data'] != current_date:
            prices_variation = get_variation(today_prices, previous_day_prices, companies_names)
            for company_name in companies_names:
                behavior_list[company_name].append(prices_variation[company_name])

            current_date = entry['Data']
            previous_day_prices = today_prices
            today_prices = {}

        today_prices[entry['Empresa']] = entry['Valor']

    pattern_map = generate_patternmap(behavior_list, companies_names)
    pattern_map = normalize_patternmap(pattern_map)
    bayesnet = compute_patterns(pattern_map)
    return bayesnet, companies_names
