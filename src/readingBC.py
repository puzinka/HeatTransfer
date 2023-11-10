import numpy as np
from findIndexByElementPart import findArrayOfIndexesByElementPart

# извлекаем из файла inp ГУ Дирихле

def getBC(fileName):
    file = open(fileName, 'r')
    lines = file.read().split('\n')

    BC = dict()
    indexes = findArrayOfIndexesByElementPart(lines, 'Type: Temperature')

    for index in indexes:
        # извлекаем узлы, на которые действуют ГУ
        nameOfSet = lines[index + 2].split(', ')[0]
        indexOfNodesBC = findArrayOfIndexesByElementPart(lines, '*Nset, nset=' + nameOfSet + ', instance') + 1
        nodesBC = np.array(lines[indexOfNodesBC].split(', '))

        # температура на границе тела
        temperature = lines[index + 2].split(', ')[-1]

        BC[float(temperature)] = nodesBC.astype(int)

    return BC