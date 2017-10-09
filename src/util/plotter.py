import json
import os
import matplotlib.pyplot as plt
import operator
from datetime import datetime

def plot_graph(company_name, input_json='data/cotacoes.json', output_graph='data/plot.png'):
    """Plots stock price variation graph into image file for displaying"""
    # TODO: Funcao para plotar grafico aqui

    allDates = []
    allValues = []
    graphData = []

    index = 0
    interval = 0 #criar func para receber o intervalo de interesse

    with open(input_json, 'r') as inputfile:
        inputData = json.load(inputfile)
        inputfile.close()

    while inputData[index]['Empresa'] != company_name:
        index += 1

    while inputData[index]['Empresa'] == company_name:
        graphData.append(inputData[index])
        interval += 1

    print("PLOTTING THE MAP...")    
    
    for i in range(len(graphData)):
        graphData[i]['Data'] = datetime.strptime(graphData[i]['Data'], "%d-%m-%Y")

    graphData.sort(key=operator.itemgetter('Data'))

    for i in range(len(graphData)):
        allDates.append(graphData[i]['Data'])
        allDates.append(graphData[i]['Data'])

    plt.figure(figsize=(13, 7))
    plt.plot(allDates, allDates, '.r-')
    plt.xlabel("Data")
    plt.ylabel("Valor (R$)")
    plt.title("Empresa: " + company_name)
    plt.grid()
    #plt.savefig('data/' + company_name + " " + str(interval) + '_days.png', dpi=100)
    plt.savefig('data/graph.png', dpi=100)
    plt.show()
