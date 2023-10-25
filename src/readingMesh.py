import numpy as np
from findIndexByElementPart import findIndexByElementPart

########### двумерный случай, модель состоит из одного part ###########

def readingMesh(fileName):
    file = open(fileName, 'r')
    lines = file.read().split('\n')

    startIndexOfNodes = lines.index('*Node') + 1
    startIndexOfElements = findIndexByElementPart(lines, '*Element') + 1
    endIndexElements = findIndexByElementPart(lines, '*Nset') - 1

    # определили количество узлов и элементов модели
    countNodes = startIndexOfElements - startIndexOfNodes - 1
    countElements = endIndexElements - startIndexOfElements + 1

    # массивы с данными об узлах и элементах
    nodes = lines[startIndexOfNodes : startIndexOfNodes + countNodes]
    elements = lines[startIndexOfElements : startIndexOfElements + countElements]

    # словари координат и элементов
    elementsLibrary = dict()
    nodesLibrary = dict()

    for element in elements:
        newElement = np.array(element.replace(' ', '').split(','))
        elementsLibrary[int(newElement[0])] = newElement[1:].astype(int)

    for node in nodes:
        newNode = np.array(node.replace(' ', '').split(','))
        nodesLibrary[int(newNode[0])] = newNode[1:].astype(float)

    return [elementsLibrary, nodesLibrary]
