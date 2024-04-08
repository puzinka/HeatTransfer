import numpy as np
from getGlobalMatrix import getGlobalMatrix

# def getHeatCapcitnceMatrix(elementsLibrary, nodesLibrary, density, specificHeat):

#     # матрица теплоёмкости
#     globalHeatCapcitnceMatrix = np.zeros([len(nodesLibrary), len(nodesLibrary)])

#     # интеграл [N]^T[N] по объёму через L-координаты
#     localMatrix = np.array([[2, 1, 1], [1, 2, 1], [1, 1, 2]])

#     for number in range(1, len(elementsLibrary) + 1):

#         coordinatesMatrix = []
#         nodeNumbers = []

#         for node in elementsLibrary[number]:
#             coordinatesMatrix.append(np.array(nodesLibrary[node]))
#             nodeNumbers.append(node - 1)

#         [[Xi, Yi], [Xj, Yj], [Xk, Yk]] = coordinatesMatrix

#         area = 0.5 * abs(Xi * (Yj - Yk) + Xj * (Yk - Yi) + Xk * (Yi - Yj))

#         [number_i, number_j, number_k] = nodeNumbers

#         localHeatCapcitnceMatrix = 1/12 * density * specificHeat * area * localMatrix
#         globalHeatCapcitnceMatrix = getGlobalMatrix(globalHeatCapcitnceMatrix, localHeatCapcitnceMatrix, number_i, number_j, number_k)

#     return globalHeatCapcitnceMatrix

def getHeatCapcitnceMatrix(elementsLibrary, nodesLibrary, density, specificHeat):

    # матрица теплоёмкости
    globalHeatCapcitnceMatrix = np.zeros([len(nodesLibrary), len(nodesLibrary)])

    localMatrix = np.array([
        [2, 1, 1], 
        [1, 2, 1],
        [1, 1, 2]
    ])

    for number in range(1, len(elementsLibrary) + 1):

        coordinatesMatrix = []
        nodeNumbers = []

        for node in elementsLibrary[number]:
            coordinatesMatrix.append(np.array(nodesLibrary[node]))
            nodeNumbers.append(node - 1)

        [number_i, number_j, number_k] = nodeNumbers
        [[Xi, Yi], [Xj, Yj], [Xk, Yk]] = coordinatesMatrix

        area = 0.5 * abs(Xi * (Yj - Yk) + Xj * (Yk - Yi) + Xk * (Yi - Yj))

        localHeatCapcitnceMatrix = 1/12 * density * specificHeat * area * localMatrix
        globalHeatCapcitnceMatrix = getGlobalMatrix(globalHeatCapcitnceMatrix, localHeatCapcitnceMatrix, number_i, number_j, number_k)

    return globalHeatCapcitnceMatrix