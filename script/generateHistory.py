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


def getFileName(filePath, version):
    fileName = filePath.split('/')[-1].split('.')[0] + '-v' + str(version + 1)
    return fileName


def getCommitHistory(filePath):
    # https://git-scm.com/docs/pretty-formats
    command = 'git log --pretty=format:"%H %as" {}'.format(filePath)
    process = Popen(command, stdout=PIPE, stderr=None, shell=True)
    output = process.communicate()[0].decode("utf-8").splitlines()
    result = []
    for commit in output:
        result.append(commit.split(' '))
    return result


def generateHistory(fileList, basePath):
    keys = ['File Name', 'commit', 'date']
    makeLine(keys)
    makeEmptyLine(keys)
    oraklConfigPath = 'https://github.com/Bisonai/orakl-config/blob/'
    for file in fileList:
        filePath = os.path.join(basePath, file)
        commitList = getCommitHistory(filePath)
        for index, commit in enumerate(commitList):
            url = '{}{}/{}'.format(oraklConfigPath, commit[0], filePath)
            fileName = getFileName(filePath, index)
            makeLine([{'url': url, 'value': fileName}, commit[0], commit[1]])


print('\n## Adapter History\n')
generateHistory(adapters, adapterPath)

print('\n## Aggregator Baobab History\n')
generateHistory(aggregatorsBaobab, aggregatorBaobabPath)

print('\n## Aggregator Default History\n')
generateHistory(aggregatorsDefault, aggregatorDefaultPath)
