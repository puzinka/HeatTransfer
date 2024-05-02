import numpy as np

from readingMesh import readingMesh
from readingMaterialProperties import getConductivity, getDensity, getSpecificHeat
from readingBC import getBC
from getConductivityMatrix import getConductivityMatrix, getConductivityMatrixOld
from applyBC import nullMatrixRow, applyBCtoF, nullMatrixCol
from getHeatCapcitnceMatrix import getHeatCapcitnceMatrix
from solveHeatTransfer import solveOfTransitiveHeatTransfer, solveOfTransitiveHeatTransferOld
from plotting2D import plotting2D

# fileName = '../fixtures/test_2_feb.inp'
# fileName = '../fixtures/feb3.inp'
# fileName = '../fixtures/200-elem.inp'

fileName = "../fixtures/1-05.inp"

[elementsLibrary, nodesLibrary] = readingMesh(fileName)

conductivity = getConductivity(fileName)
density = getDensity(fileName)
specificHeat = getSpecificHeat(fileName)

# conductivity = 1.3


# BC = getBC(fileName)

conductivityMatrix = getConductivityMatrixOld(elementsLibrary, nodesLibrary, conductivity)
force = np.zeros(len(nodesLibrary))

# #применение ГУ
# matrixK = nullMatrixRow(condictivityMatrixWithoutBC, BC)
# force1 = applyBCtoF(matrixK, forceWithoutBC, BC)
# conductivityMatrix = nullMatrixCol(matrixK, BC)

# capcitnceMatrix = getHeatCapcitnceMatrix(elementsLibrary, nodesLibrary, density, specificHeat)
capcitnceMatrix = getHeatCapcitnceMatrix(elementsLibrary, nodesLibrary, density, specificHeat)

# matrixC = nullMatrixRow(capcitnceMatrixWithoutBC, BC)
# force = applyBCtoF(matrixC, force1, BC)
# capcitnceMatrix = nullMatrixCol(matrixC, BC)


initialT = np.zeros(len(force))

timeStep = 1
countStep = 10000

temperature = solveOfTransitiveHeatTransferOld(initialT, capcitnceMatrix, conductivityMatrix, force)


i = countStep - 1
plotting2D(elementsLibrary, nodesLibrary, temperature[i])

for i in temperature[-1]:
    print(i)