import os
import json

adapterPath = '/Users/bayram/Git/orakl-config/adapter'
aggregatorPath = '/Users/bayram/Git/orakl-config/aggregator/default'

adapters = sorted(os.listdir(adapterPath))
aggregators = sorted(os.listdir(aggregatorPath))

adapterUrl = "https://bisonai.github.io/orakl-config/adapter/"
aggregatorUrl = "https://bisonai.github.io/orakl-config/aggregator/default/"


def makeLine(words):
    for word in words:
        if type(word) != dict:
            if word == '':
                word = '-'
            print('| {} '.format(word), end='')
        else:
            print('| [{}]({}) '.format(word['value'], word['url']), end='')
    print(' |')


def makeEmptyLine(words):
    for i in range(len(words)):
        print('| ', '---', end=' ')
    print(' |')


def generateAdapterList():
    keys = ['name', 'adapterHash', 'decimals', 'feeds']
    makeLine(keys)
    makeEmptyLine(keys)
    for adapter in adapters:
        filePath = os.path.join(adapterPath, adapter)
        with open(filePath) as json_file:
            data = json.load(json_file)
        values = []
        for key in keys:
            if key == 'feeds':
                values.append(len(data[key]))
            elif key == 'name':
                values.append({'url': adapterUrl + adapter, 'value': data[key]})
            else:
                values.append(data[key])
        makeLine(values)


def generateAggregatorList():
    keys = ['name', 'aggregatorHash', 'address', 'heartbeat', 'threshold', 'absoluteThreshold', 'adapterHash']
    makeLine(keys)
    makeEmptyLine(keys)
    for aggregator in aggregators:
        filePath = os.path.join(aggregatorPath, aggregator)
        with open(filePath) as json_file:
            data = json.load(json_file)
        values = []
        for key in keys:
            if key == 'feeds':
                values.append(len(data[key]))
            elif key == 'name':
                values.append({'url': aggregatorUrl + aggregator, 'value': data[key]})
            else:
                values.append(data[key])
        makeLine(values)


print('# Orakl Config\n')
print('## Adapter List\n')
generateAdapterList()
print('## Aggregator List\n')
generateAggregatorList()
