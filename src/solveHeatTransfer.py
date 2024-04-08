from decimal import Decimal, getcontext

import numpy as np
import numpy.linalg as la

# from readingBC import getBC
# from applyBC import applyBCtoVector
# from convertToDecimal import convertToDecimalMatrix, convertToDecimalVector, convertToDecimalNumber
# from operationsMatrix import multiplyMatrixToMatrix, multiplyMatrixToVector, sumVectors, subVectors, multiplyNumberToVector

# # fileName = '../fixtures/december10.inp'
# fileName = '../fixtures/december10.inp'
# # fileName = '../fixtures/test_2_feb.inp'
# BC = getBC(fileName)


# решение стационарной задачи теплопроводности

def solveOfSteadyStateHeatTransfer(conductivityMatrixWithBC, thermalForceWithBC):
    temperature = la.solve(conductivityMatrixWithBC,thermalForceWithBC)
    return temperature


# решение нестационарной задачи теплопроводности

def solveOfTransitiveHeatTransfer(initialT, capcitnceMatrix, conductivityMatrix, force, timeStep, countStep, BC):
    
    temperatureMoments = []

    # T1 = initialT
    # temperatureMoments.append(T1)

    # A = 0.5 * capcitnceMatrix + timeStep * (1/6) * conductivityMatrix
    # B1 = 0.5 * force - np.dot((timeStep * (1/3) * conductivityMatrix - 0.5 * capcitnceMatrix), T1)
    # T2 = np.linalg.solve(A, B1)
    # temperatureMoments.append(T2)

    # for i in range(1, countStep):
    #     B = -force - (2/3) * timeStep * np.dot(conductivityMatrix, T2) - np.dot((timeStep * (1/6) * conductivityMatrix - 0.5 * capcitnceMatrix), T1)
    #     T3 = np.linalg.solve(A, B)

    #     temperatureMoments.append(T3)

    #     T1 = T2
    #     T2 = T3

    temperatureMoments.append(initialT)

    invC = np.linalg.inv(capcitnceMatrix)

    for i in range(1, countStep):
        T = initialT - timeStep * np.dot(np.dot(invC, conductivityMatrix), initialT) + timeStep * np.dot(invC, force)

        for temperature in BC:
            for node in BC[temperature]:
                T[int(node) - 1] = temperature

        temperatureMoments.append(T)

        initialT = T

    return temperatureMoments

# def solveOfTransitiveHeatTransfer(initialTemperature, heatCapcitnceMatrixWithBC, conductivityMatrixWithBC, thermalForceWithBC, timeStep):

#     temperatureMoments = []
#     temperatureMoments.append(initialTemperature)

#     diff = 100
#     stepNumber = 1

#     while diff > 0.1:

#         # A*X=B
#         A = 0.5 * heatCapcitnceMatrixWithBC + (timeStep * stepNumber / 6) * conductivityMatrixWithBC
#         B = 0.5 * thermalForceWithBC - np.matmul((-0.5 * heatCapcitnceMatrixWithBC + (timeStep * stepNumber / 3) * conductivityMatrixWithBC), initialTemperature)

#         temperature = la.solve(A, B)
#         temperatureMoments.append(temperature)

#         diff = max(abs(temperatureMoments[-2] - temperatureMoments[-1]))

#         stepNumber += 1

#     return temperatureMoments

# tmp = {0: 30, 1: 28, 2: 26, 3: 24, 4: 22, 5: 20, 6: 18, 7: 16, 8: 14, 9: 12, 10: 10}


# def solveOfTransitiveHeatTransfer(initialTemperature, heatCapcitnceMatrixWithBC, conductivityMatrixWithBC, thermalForceWithBC, timeStep):

#     temperatureMoments = []
#     # temperatureMoments.append(initialTemperature)

#     stepNumber = 1

#     tetta = 0.5

#     temperatureMoments.append(initialTemperature)

#     force1 = thermalForceWithBC
#     force2 = thermalForceWithBC

#     for step in range(len(tmp) - 1):
     
#         for node in BC[1.0]:
#             force1[node - 1] = tmp[step]
#             force2[node - 1] = tmp[step + 1]

#         force = force1 + tetta * (force2 - force1)

#         # K*X=F
#         K = heatCapcitnceMatrixWithBC + timeStep * tetta * conductivityMatrixWithBC
#         F = np.dot(heatCapcitnceMatrixWithBC - timeStep * (1 - tetta) * conductivityMatrixWithBC, initialTemperature) + timeStep * force

#         temperature = la.solve(K, F)

#         temperatureMoments.append(temperature)

#         initialTemperature = temperature

#         stepNumber += 1

#     return temperatureMoments


# -----------------------------------------------------------------по Сегерлинду 

# def solveOfTransitiveHeatTransfer(initialTemperature, heatCapcitnceMatrixWithBC, conductivityMatrixWithBC, thermalForceWithBC, timeStep):

#     temperatureMoments = []
#     # temperatureMoments.append(initialTemperature)

#     stepNumber = 1

#     temperature1 = initialTemperature
#     temperatureMoments.append(temperature1)

#     for node in BC[1.0]:
#         thermalForceWithBC[node - 1] = tmp[0]

#     A = 0.5 * heatCapcitnceMatrixWithBC + (timeStep / 6) * conductivityMatrixWithBC
#     B = 0.5 * thermalForceWithBC - np.matmul((-0.5 * heatCapcitnceMatrixWithBC + (timeStep / 3) * conductivityMatrixWithBC), initialTemperature)
#     temperature2 = la.solve(A, B)
#     temperatureMoments.append(temperature2)

#     ###
#     thermalForceInitial = thermalForceWithBC
#     ###

#     for step in range(1, len(tmp)):
     
#         for node in BC[1.0]:
#             thermalForceWithBC[node - 1] = tmp[step]

#         ###
#         thermalForceDiff = -thermalForceWithBC + thermalForceInitial
#         ###

#         # A*X=B
#         # A = 0.5 * heatCapcitnceMatrixWithBC + (timeStep * stepNumber / 6) * conductivityMatrixWithBC
#         # B = 0.5 * thermalForceWithBC - np.matmul((-0.5 * heatCapcitnceMatrixWithBC + (timeStep * stepNumber / 3) * conductivityMatrixWithBC), initialTemperature)

#         # A = 0.5 * heatCapcitnceMatrixWithBC + (timeStep / 6) * conductivityMatrixWithBC
#         # B = thermalForceWithBC - np.matmul((-0.5 * heatCapcitnceMatrixWithBC + (timeStep / 6) * conductivityMatrixWithBC), temperature1) - (2 / 3) * timeStep * np.matmul(conductivityMatrixWithBC, temperature2)

#         A = 0.5 * heatCapcitnceMatrixWithBC + (timeStep / 6) * conductivityMatrixWithBC
#         B = thermalForceDiff - np.matmul((-0.5 * heatCapcitnceMatrixWithBC + (timeStep / 6) * conductivityMatrixWithBC), temperature1) - (2 / 3) * timeStep * np.matmul(conductivityMatrixWithBC, temperature2)
        
#         temperature3 = la.solve(A, B)

#         temperatureMoments.append(temperature3)

#         temperature1 = temperature2
#         temperature2 = temperature3

#         stepNumber += 1

#     return temperatureMoments


#-------------------------------------------по Сегерлинду с модификацией

# def solveOfTransitiveHeatTransfer(initialTemperature, heatCapcitnceMatrixWithBC, conductivityMatrixWithBC, thermalForceWithBC, timeStep):

#     temperatureMoments = []
#     # temperatureMoments.append(initialTemperature)

#     stepNumber = 1

#     temperature = initialTemperature
#     temperatureMoments.append(temperature)

#     for step in tmp:
     
#         for node in BC[1.0]:
#             thermalForceWithBC[node - 1] = tmp[step]

#         # A*X=B
#         A = 0.5 * heatCapcitnceMatrixWithBC + (timeStep * stepNumber / 6) * conductivityMatrixWithBC
#         B = 0.5 * thermalForceWithBC - np.matmul((-0.5 * heatCapcitnceMatrixWithBC + (timeStep * stepNumber / 3) * conductivityMatrixWithBC), initialTemperature)

#         temperature = la.solve(A, B)

#         temperatureMoments.append(temperature)

#         stepNumber += 1

#     return temperatureMoments


# ------------------------------------------ Прямой Эйлера

# def solveOfTransitiveHeatTransfer(initialTemperature, heatCapcitnceMatrixWithBC, conductivityMatrixWithBC, thermalForceWithBC, timeStep):

#     temperatureMoments = []

#     # stepNumber = 1

#     temperatureMoments.append(initialTemperature)

#     for step in tmp:
     
#         for node in BC[1.0]:
#             thermalForceWithBC[node - 1] = tmp[step]

#         # A*X=B
#         A = heatCapcitnceMatrixWithBC
#         B = np.dot(heatCapcitnceMatrixWithBC, initialTemperature) - timeStep * np.dot(conductivityMatrixWithBC, initialTemperature) + timeStep * thermalForceWithBC

#         temperature = la.solve(A, B)

#         temperatureMoments.append(temperature)

#         initialTemperature = temperature

#         # stepNumber += 1

#     return temperatureMoments
