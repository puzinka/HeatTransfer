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

tmp = {0: 30, 1: 28, 2: 26, 3: 24, 4: 22, 5: 20, 6: 18, 7: 16, 8: 14, 9: 12, 10: 10}

def solveOfTransitiveHeatTransfer(initialTemperature, heatCapcitnceMatrixWithBC, conductivityMatrixWithBC, thermalForceWithBC, timeStep):

    temperatureMoments = []
    temperatureMoments.append(initialTemperature)

    stepNumber = 1

    for step in tmp:
     
        for node in BC[1.0]:
            thermalForceWithBC[node - 1] = tmp[step]

        # A*X=B
        A = 0.5 * heatCapcitnceMatrixWithBC + (timeStep * stepNumber / 6) * conductivityMatrixWithBC
        B = 0.5 * thermalForceWithBC - np.matmul((-0.5 * heatCapcitnceMatrixWithBC + (timeStep * stepNumber / 3) * conductivityMatrixWithBC), initialTemperature)

        temperature = la.solve(A, B)
        temperatureMoments.append(temperature)

        diff = max(abs(temperatureMoments[-2] - temperatureMoments[-1]))

        stepNumber += 1

    return temperatureMoments
