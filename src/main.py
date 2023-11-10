import numpy as np

from readingMesh import readingMesh
from getConductivityMatrix import getConductivityMatrix
from plotting2D import plotting2D
from readingBC import getBC
from applyBC import applyBCtoMatrix, applyBCtoVector
from readingMaterialProperties import getConductivity, getDensity, getSpecificHeat
from getHeatCapcitnceMatrix import getHeatCapcitnceMatrix
from solveHeatTransfer import solveOfSteadyStateHeatTransfer, solveOfTransitiveHeatTransfer


# fileName = '../fixtures/Thermal.inp'
fileName = '../fixtures/dam_heat-transfer_test.inp'
[elementsLibrary, nodesLibrary] = readingMesh(fileName)


# Стационарная 2D задача -------------------------------------------------------------#

conductivity = getConductivity(fileName)

BC = getBC(fileName)

globalCondictivityMatrix = getConductivityMatrix(elementsLibrary, nodesLibrary, conductivity)
conductivityMatrixWithBC = applyBCtoMatrix(globalCondictivityMatrix, BC)

thermalForce = np.zeros(len(nodesLibrary))
thermalForceWithBC = applyBCtoVector(thermalForce, BC)

temperature = solveOfSteadyStateHeatTransfer(conductivityMatrixWithBC, thermalForceWithBC)

# plotting2D(elementsLibrary, nodesLibrary, temperature)


# Нестационарная 2D задача -----------------------------------------------------------#

density = getDensity(fileName)
specificHeat = getSpecificHeat(fileName)

globalHeatCapcitnceMatrix= getHeatCapcitnceMatrix(elementsLibrary, nodesLibrary, density, specificHeat)
heatCapcitnceMatrixWithBC = applyBCtoMatrix(globalHeatCapcitnceMatrix, BC)

timeStep = 0.0001
initialTemperature = np.zeros(len(thermalForceWithBC))

temperature = solveOfTransitiveHeatTransfer(initialTemperature, heatCapcitnceMatrixWithBC, conductivityMatrixWithBC, thermalForceWithBC, timeStep)

print(temperature)
plotting2D(elementsLibrary, nodesLibrary, temperature[1])




