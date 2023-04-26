import json
import os
from subprocess import PIPE, Popen

adapterPath = 'adapter/'
aggregatorDefaultPath = 'aggregator/default/'
aggregatorBaobabPath = 'aggregator/baobab/'

adapters = sorted(os.listdir(adapterPath))
aggregatorsDefault = sorted(os.listdir(aggregatorDefaultPath))
aggregatorsBaobab = sorted(os.listdir(aggregatorBaobabPath))


def loadJsonFromPath(filePath):
    with open(filePath) as json_file:
        data = json.load(json_file)
    return data


def makeLine(words):
    for word in words:
        if type(word) == dict:
            print('| [{}]({}) '.format(word['value'], word['url']), end='')
        elif type(word) == list:
            print('| ', end='')
            for version in word:
                print('[{}]({})'.format(version['value'], version['url']), end='')
                if version != word[-1]:
                    print(', ', end='')
        else:
            if word == '':
                word = '-'
            print('| {} '.format(word), end='')
    print(' |')


def makeEmptyLine(words):
    for i in range(len(words)):
        print('| ', '---', end=' ')
    print(' |')


def getUrlList(filePath):
    # https://git-scm.com/docs/pretty-formats
    command = 'git log --branches master --pretty=format:"%H" {}'.format(filePath)
    process = Popen(command, stdout=PIPE, stderr=None, shell=True)
    commitList = process.communicate()[0].decode("utf-8").splitlines()

    oraklConfigPath = 'https://github.com/Bisonai/orakl-config/blob/'
    urlList = []

    for index, commit in enumerate(commitList):
        url = '{}{}/{}'.format(oraklConfigPath, commit, filePath)
        version = 'v' + str(index + 1)
        urlList.append({'url': url, 'value': version})
    return urlList


def getFileName(filePath):
    data = loadJsonFromPath(filePath)
    return data['name']


def generateHistory(fileList, basePath):
    keys = ['File Name', 'History']
    makeLine(keys)
    makeEmptyLine(keys)
    for file in fileList:
        filePath = os.path.join(basePath, file)
        fileName = getFileName(filePath)
        urlList = getUrlList(filePath)
        makeLine([fileName, urlList])


print('\n# History of Adapter and Aggregator')

print('\n## Adapter\n')
generateHistory(adapters, adapterPath)

print('\n## Aggregator Baobab\n')
generateHistory(aggregatorsBaobab, aggregatorBaobabPath)

print('\n## Aggregator Default\n')
generateHistory(aggregatorsDefault, aggregatorDefaultPath)
