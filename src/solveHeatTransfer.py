import numpy as np
import numpy.linalg as la

from readingBC import getBC

fileName = '../fixtures/december10.inp'
BC = getBC(fileName)


# решение стационарной задачи теплопроводности

def solveOfSteadyStateHeatTransfer(conductivityMatrixWithBC, thermalForceWithBC):
    temperature = la.solve(conductivityMatrixWithBC,thermalForceWithBC)
    return temperature


# решение нестационарной задачи теплопроводности

def solveOfTransitiveHeatTransfer(initialTemperature, heatCapcitnceMatrixWithBC, conductivityMatrixWithBC, thermalForceWithBC, timeStep):

    temperatureMoments = []
    temperatureMoments.append(initialTemperature)

    diff = 100
    stepNumber = 1

    while diff > 0.1:

        # A*X=B
        A = 0.5 * heatCapcitnceMatrixWithBC + (timeStep * stepNumber / 6) * conductivityMatrixWithBC
        B = 0.5 * thermalForceWithBC - np.matmul((-0.5 * heatCapcitnceMatrixWithBC + (timeStep * stepNumber / 3) * conductivityMatrixWithBC), initialTemperature)

        temperature = la.solve(A, B)
        temperatureMoments.append(temperature)

        diff = max(abs(temperatureMoments[-2] - temperatureMoments[-1]))

        stepNumber += 1

    return temperatureMoments

tmp = {0: 30, 1: 28, 2: 26, 3: 24, 4: 22, 5: 20, 6: 18, 7: 16, 8: 14, 9: 12, 10: 10}

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
