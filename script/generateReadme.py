import os
import json

adapterPath = 'adapter/'
aggregatorDefaultPath = 'aggregator/default/'
aggregatorBaobabPath = 'aggregator/baobab/'

adapters = sorted(os.listdir(adapterPath))
aggregatorsDefault = sorted(os.listdir(aggregatorDefaultPath))
aggregatorsBaobab = sorted(os.listdir(aggregatorBaobabPath))


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


def loadJsonFromPath(filePath):
    with open(filePath) as json_file:
        data = json.load(json_file)
    return data


def generateAdapterList():
    keys = ['name', 'adapterHash', 'decimals', 'feeds']
    makeLine(keys)
    makeEmptyLine(keys)
    for adapter in adapters:
        filePath = os.path.join(adapterPath, adapter)
        data = loadJsonFromPath(filePath)
        values = []
        for key in keys:
            if key == 'feeds':
                values.append(len(data[key]))
            elif key == 'name':
                values.append({'url': filePath, 'value': data[key]})
            else:
                values.append(data[key])
        makeLine(values)


def generateAggregatorList(aggregatorBasePath, aggregators):
    keys = ['name', 'aggregatorHash', 'address', 'heartbeat', 'threshold', 'absoluteThreshold', 'adapterHash']
    makeLine(keys)
    makeEmptyLine(keys)
    for aggregator in aggregators:
        filePath = os.path.join(aggregatorBasePath, aggregator)
        data = loadJsonFromPath(filePath)
        values = []
        for key in keys:
            if key == 'feeds':
                values.append(len(data[key]))
            elif key == 'name':
                values.append({'url': filePath, 'value': data[key]})
            else:
                values.append(data[key])
        makeLine(values)


def checkHashMatch():
    for i in range(len(adapters)):
        adapter = adapters[i]
        adapterFilePath = os.path.join(adapterPath, adapter)
        adapterData = loadJsonFromPath(adapterFilePath)

        aggregator = aggregatorsDefault[i]
        aggregatorFilePath = os.path.join(aggregatorDefaultPath, aggregator)
        aggregatorData = loadJsonFromPath(aggregatorFilePath)
        if adapterData['name'] != aggregatorData['name']:
            msg = "Wrong file Name or Price feed name, Adapter:{} Aggregator: {}".format(adapter, aggregator)
            raise Exception(msg)

        if adapterData['adapterHash'] != aggregatorData['adapterHash']:
            print('\n\n------------------------')
            print('Adapter hash values does not match')
            print("Adapter file:", adapter, adapterData['adapterHash'])
            print("Aggregator file:", aggregator, aggregatorData['adapterHash'])
            print()
            msg = "Adapter hash values does not match, Adapter:{} Aggregator: {}".format(adapter, aggregator)
            raise Exception(msg)


checkHashMatch()

print('# Orakl Config\n')
print('## Adapter\n')
generateAdapterList()
print('## Aggregator Baobab\n')
generateAggregatorList(aggregatorBaobabPath, aggregatorsBaobab)
print('## Aggregator Default\n')
generateAggregatorList(aggregatorDefaultPath, aggregatorsDefault)
