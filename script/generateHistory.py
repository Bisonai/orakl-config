import os
from subprocess import PIPE, Popen

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


def generateHistory(fileList, basePath):
    keys = ['File Name', 'commit']
    makeLine(keys)
    makeEmptyLine(keys)
    oraklConfigPath = 'https://github.com/Bisonai/orakl-config/blob/'
    for file in fileList:

        filePath = os.path.join(basePath, file)
        command = 'git log --pretty=format:"%H" {}'.format(filePath)
        process = Popen(command, stdout=PIPE, stderr=None, shell=True)
        output = process.communicate()[0].decode("utf-8").splitlines()

        # print(filePath, output)
        for commit in output:
            url = '{}{}/{}'.format(oraklConfigPath, commit, filePath)
            makeLine([{'url': url, 'value': filePath}, commit])


print('\n## Adapter History\n')
generateHistory(adapters, adapterPath)

print('\n## Aggregator Baobab History\n')
generateHistory(aggregatorsBaobab, aggregatorBaobabPath)

print('\n## Aggregator Default History\n')
generateHistory(aggregatorsDefault, aggregatorDefaultPath)
