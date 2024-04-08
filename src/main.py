import numpy as np

from readingMesh import readingMesh
from readingMaterialProperties import getConductivity, getDensity, getSpecificHeat
from readingBC import getBC
from getConductivityMatrix import getConductivityMatrix
from applyBC import nullMatrixRow, applyBCtoF, nullMatrixCol
from getHeatCapcitnceMatrix import getHeatCapcitnceMatrix
from solveHeatTransfer import solveOfTransitiveHeatTransfer
from plotting2D import plotting2D

# fileName = '../fixtures/test_2_feb.inp'
fileName = '../fixtures/feb3.inp'
# fileName = '../fixtures/200-elem.inp'

fileName = "../fixtures/Job-8.inp"

[elementsLibrary, nodesLibrary] = readingMesh(fileName)

# conductivity = getConductivity(fileName)
density = getDensity(fileName)
specificHeat = getSpecificHeat(fileName)

conductivity = 1.3


BC = getBC(fileName)

condictivityMatrixWithoutBC = getConductivityMatrix(elementsLibrary, nodesLibrary, conductivity)
forceWithoutBC = np.zeros(len(nodesLibrary))

#применение ГУ
matrixK = nullMatrixRow(condictivityMatrixWithoutBC, BC)
force1 = applyBCtoF(matrixK, forceWithoutBC, BC)
conductivityMatrix = nullMatrixCol(matrixK, BC)

# capcitnceMatrix = getHeatCapcitnceMatrix(elementsLibrary, nodesLibrary, density, specificHeat)
capcitnceMatrixWithoutBC = getHeatCapcitnceMatrix(elementsLibrary, nodesLibrary, density, specificHeat)

force = force1
# matrixC = nullMatrixRow(capcitnceMatrixWithoutBC, BC)
# force = applyBCtoF(matrixC, force1, BC)
# capcitnceMatrix = nullMatrixCol(matrixC, BC)
capcitnceMatrix = capcitnceMatrixWithoutBC

initialT = np.zeros(len(force))

timeStep = 1
countStep = 10

temperature = solveOfTransitiveHeatTransfer(initialT, capcitnceMatrix, conductivityMatrix, force, timeStep, countStep, BC)

print(BC)

i = countStep - 1
plotting2D(elementsLibrary, nodesLibrary, temperature[i])

