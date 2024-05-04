import numpy as np

from readingMesh import readingMesh
from readingMaterialProperties import getConductivity, getDensity, getSpecificHeat
# from readingBC import getBC
from getConductivityMatrix import getConductivityMatrix
# from applyBC import nullMatrixRow, applyBCtoF, nullMatrixCol
from getHeatCapcitnceMatrix import getHeatCapcitnceMatrix
from convertToDecimal import convertToDecimalVector, convertToDecimalNumber
from solveHeatTransfer import solveOfTransitiveHeatTransfer, solveOfSteadyStateHeatTransfer
from plotting2D import plotting2D


# fileName = '../fixtures/test_20_04.inp'
fileName = '../fixtures/1-05.inp'

flag = False

[elementsLibrary, nodesLibrary] = readingMesh(fileName)

conductivity = getConductivity(fileName)
# conductivity = 22464

density = getDensity(fileName)
specificHeat = getSpecificHeat(fileName)

conductivityMatrix = getConductivityMatrix(elementsLibrary, nodesLibrary, conductivity, flag)

if flag:
    force = convertToDecimalVector(np.zeros(len(nodesLibrary)))
    initialT = convertToDecimalVector(np.zeros(len(force)))
else:
    force = np.zeros(len(nodesLibrary))
    initialT = np.zeros(len(force))

capcitnceMatrix = getHeatCapcitnceMatrix(elementsLibrary, nodesLibrary, density, specificHeat)


temperature = solveOfTransitiveHeatTransfer(initialT, capcitnceMatrix, conductivityMatrix, force, flag)

for i in temperature[-1]:
    print(i)


# print('node 3148')
# for step in temperature:
#     print(step[3147])

# print('node 2559')
# for step in temperature:
#     print(step[2558])

# print('node 2396')
# for step in temperature:
#     print(step[2395])

# print('node 2238')
# for step in temperature:
#     print(step[2237])


# plotting2D(elementsLibrary, nodesLibrary, initialT)
# plotting2D(elementsLibrary, nodesLibrary, temperature[i])

# стационарная

# temperature = solveOfSteadyStateHeatTransfer(conductivityMatrix, force, flag)

# for i in temperature:
#     print(i)

# plotting2D(elementsLibrary, nodesLibrary, temperature)