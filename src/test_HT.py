import numpy as np

from readingMesh import readingMesh
from getConductivityMatrix import getConductivityMatrix
from plotting2D import plotting2D
from readingBC import getBC
from applyBC import applyBCtoMatrix, applyBCtoVector
from readingMaterialProperties import getConductivity, getDensity, getSpecificHeat
from getHeatCapcitnceMatrix import getHeatCapcitnceMatrix
from solveHeatTransfer import solveOfSteadyStateHeatTransfer, solveOfTransitiveHeatTransfer
from convertToDecimal import convertToDecimalMatrix

from decimal import Decimal, getcontext

getcontext().prec = 1000

# 1. Необходимо собрать уравнение теплопроводности. Для этого соберем матрицы 
#    теплопроводности K и матрицу теплоёмкости C.

# fileName = '../fixtures/test_2_feb.inp'
fileName = '../fixtures/feb3.inp'
[elementsLibrary, nodesLibrary] = readingMesh(fileName)

conductivity = getConductivity(fileName)
density = getDensity(fileName)
specificHeat = getSpecificHeat(fileName)

# conductivity = 1.2
# density = 1500
# specificHeat = 0.9

BC = getBC(fileName)

# K
globalCondictivityMatrix = getConductivityMatrix(elementsLibrary, nodesLibrary, conductivity)
conductivityMatrix = applyBCtoMatrix(globalCondictivityMatrix, BC)

# C
globalHeatCapcitnceMatrix = getHeatCapcitnceMatrix(elementsLibrary, nodesLibrary, density, specificHeat)
heatCapcitnceMatrix = applyBCtoMatrix(globalHeatCapcitnceMatrix, BC)

# F
thermalForce = np.zeros(len(nodesLibrary))
thermalF = applyBCtoVector(thermalForce, BC)

# T0
initialT = np.zeros(len(thermalForce))
initialT = thermalF

timeStep = 100
temp = solveOfTransitiveHeatTransfer(initialT, heatCapcitnceMatrix, conductivityMatrix, thermalF, timeStep)

# print(temp)

i = 1
# for j in range(i):
#     print(min(temp[j]))

plotting2D(elementsLibrary, nodesLibrary, temp[i])

# print(temp[i][20])
# for i in range(1,len(temp)) :  
#     plotting2D(elementsLibrary, nodesLibrary, temp[i])