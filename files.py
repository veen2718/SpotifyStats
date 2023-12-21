from json import loads, dumps
from os import listdir, mkdir

def readJson(name):
    with open(name, 'r') as json_file:
        data = loads(json_file.read())
        return data
    

def writeJson(name, data):
    with open(name, 'w') as json_file:
        json_file.write(dumps(data,indent=4))


def setupFiles():
    if 'data' not in listdir():
        mkdir('data')
    filesPaths = [
        ['data','history.json'],
        ['data','logs.json'],
    ]

    for folder, file in filesPaths:
        if file not in listdir(folder):
            writeJson(f'{folder}/{file}',[])
    
    if 'temp' not in listdir():
        mkdir('temp')