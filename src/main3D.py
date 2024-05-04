import numpy as np

from readingMesh import readingMesh
from readingMaterialProperties import getConductivity, getDensity, getSpecificHeat
# # from readingBC import getBC
from getConductivityMatrix import getConductivityMatrix3D
# # from applyBC import nullMatrixRow, applyBCtoF, nullMatrixCol
from getHeatCapcitnceMatrix import getHeatCapcitnceMatrix, getHeatCapcitnceMatrix3D
# from convertToDecimal import convertToDecimalVector, convertToDecimalNumber
from solveHeatTransfer import solveOfTransitiveHeatTransfer, solveOfSteadyStateHeatTransfer
# from plotting2D import plotting2D

fileName = '../fixtures/3d-28-04.inp'
# fileName = '../fixtures/3d-10m.inp'

flag = False

[elementsLibrary, nodesLibrary] = readingMesh(fileName)

conductivity = getConductivity(fileName)
# conductivity = 1
density = getDensity(fileName)
# density = 1
specificHeat = getSpecificHeat(fileName)
# specificHeat = 100

conductivityMatrix = getConductivityMatrix3D(elementsLibrary, nodesLibrary, conductivity)

force = np.zeros(len(nodesLibrary))
initialT = np.zeros(len(force))

capcitnceMatrix = getHeatCapcitnceMatrix3D(elementsLibrary, nodesLibrary, density, specificHeat)

# temperature = solveOfTransitiveHeatTransfer(initialT, capcitnceMatrix, conductivityMatrix, force, flag)

# print(max(temperature[-1]))

# print(temperature)

# for node in temperature[-1]:
#     print(node)

# стационарная

temperature = solveOfSteadyStateHeatTransfer(conductivityMatrix, force, flag)

for i in temperature:
    print(i)
