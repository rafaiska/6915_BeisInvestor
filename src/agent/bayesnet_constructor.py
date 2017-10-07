def fetch_companies_names(hist_json):
    names = set()
    for entry in hist_json:
        names.add(entry['Empresa'])
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
        percentual_variation = (today[company_name] - previous[company_name]) / previous[company_name]
        percentual_variation *= 100.0

        if percentual_variation > 5.0:
            variation[company_name] = 'u'
        elif percentual_variation < -5.0:
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

    for i in range(length -1):
        pattern_string = ''
        for company_name in blists:
            pattern_string += blists[company_name][i]
        for company_name in blists:
            if blists[company_name][i + 1] == 'n':
                continue
            if pattern_string not in patternmap[company_name].keys():
                patternmap[company_name][pattern_string] = []
            patternmap[company_name][pattern_string].append(blists[company_name][i+1])
    return patternmap

def normalize_patternmap(pattern_map):
    def findall_n(pattern):
        all_found = []
        start = 0
        end = len(pattern)
        found = pattern.find('n', start, end)
        while found != -1:
            all_found.append(found)
            start = found + 1
            found = pattern.find('n', start, end)
        return all_found

    pass

def compute_patterns(pattern_map):
    bayesnet = {}

    for company_name in pattern_map:
        bayesnet[company_name] = {}
        for pattern in pattern_map[company_name]:
            if pattern.count('n') > 3:
                continue
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
    bayesnet = compute_patterns(pattern_map)
    print(bayesnet)


