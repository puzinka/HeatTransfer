from readingMesh import readingMesh

fileName = '../fixtures/Thermal.inp'

[elementsLibrary, nodesLibrary] = readingMesh(fileName)

print('Элементы и их узлы:')
print(elementsLibrary)
print('Узлы и их координаты (x, y):')
print(nodesLibrary)