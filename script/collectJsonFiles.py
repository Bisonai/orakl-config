import json
import os

adapterPath = 'adapter/'

adapters = sorted(os.listdir(adapterPath))

def loadJsonFromPath(filePath):
    with open(filePath) as json_file:
        data = json.load(json_file)
    return data

def collectJsonFiles(fileList):
    result = []
    for file in fileList:
        if 'PEG-POR' not in file:
            filePath = os.path.join(adapterPath, file)
            data = loadJsonFromPath(filePath)
            result.append(data)
    with open("collection.json", "w") as f:
        json.dump({"adapters": result}, f)

collectJsonFiles(adapters)