import math

# import requests module
import requests

# api-endpoint
URL = 'https://frankfurter.app'

# sending get request and saving the response as response object
currencies = requests.get(url=URL+'/currencies')

# extracting data in json format
currenciesObject = currencies.json()

# should contain list of currencies e.g. ['USD', 'BRL' ]
currencyCodesArray = []

# should contain table with currency pairs and exchange rates e.g. { "USD_JPY": "88.3656587", "USD_USD": "1.0000000",  }
currencyTableEdges = {}

# populate currency codes list
for currencyCode, currencyFullName in currenciesObject.items():
    currencyCodesArray.append(currencyCode)


print("Please wait while generating currency pair table ")
# populate currencyTableEdges
for pairPartOne in currencyCodesArray:
    for pairPartTwo in currencyCodesArray:
        if pairPartOne == pairPartTwo:
            currencyTableEdges.update({pairPartOne+"_"+pairPartTwo:"1.0"})
            print(".")

        else:
            requestURL = URL+'/latest?base='+pairPartOne+'&symbols='+pairPartTwo

            # pair exchange rate request
            pairExchangeRate = requests.get(url=requestURL)

            # pair exchange rate value
            pairExchangeRateValue = pairExchangeRate.json()

            exchangeRate=str(pairExchangeRateValue['rates'][pairPartTwo])

            currencyTableEdges.update({pairPartOne+"_"+pairPartTwo:exchangeRate})

            print(".")


print(currencyTableEdges)


edges = currencyTableEdges

edge_sets = [set(k.split("_")) for k, v in edges.items()]
vertices = set.union(*edge_sets)


def arbit(src):


    dist = {v:float("inf") for v in vertices}
    pre = {v:None for v in vertices}
    dist[src] = 0
    v = len(vertices)
    e = len(edges)

    for i in range(v-1):
        for edge, wt in edges.items():
            wt = -math.log(float(wt))
            u,v = edge.split("_")
            if dist[v] > dist[u] + wt:
                dist[v] = dist[u] + wt
                pre[v] = u


    for edge, wt in edges.items():

        if dist[u] + (-math.log(float(wt))) < dist[v]:
            curr = src
            path = []
            while curr != v:
                path.append(curr)
                curr = pre[curr]
            path.extend([curr, src])
            joinstring = ' -> '
            pathwithrate = ["1 "+path[0]]
            pathLength = len(path)
            for i ,baseCurrency in enumerate(path):
                if i < pathLength-1:
                    pathwithrate.append(edges[baseCurrency+"_"+path[i+1]]+" "+path[i+1])

            print(joinstring.join(pathwithrate))

            return
                
while True:

    currency = input(" \nEnter currency symbol e.g. USD :  ")
    arbit(currency)

