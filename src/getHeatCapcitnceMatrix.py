import numpy as np
from getGlobalMatrix import getGlobalMatrix, getGlobalMatrix3D


def getHeatCapcitnceMatrix3D(elementsLibrary, nodesLibrary, density, specificHeat):

    # матрица теплоёмкости
    globalHeatCapcitnceMatrix = np.zeros([len(nodesLibrary), len(nodesLibrary)])

    localMatrix = np.array([
        [2, 1, 1, 1], 
        [1, 2, 1, 1],
        [1, 1, 2, 1],
        [1, 1, 1, 2]
    ])

    for number in range(1, len(elementsLibrary) + 1):

        coordinatesMatrix = []
        nodeNumbers = []

        for node in elementsLibrary[number]:
            coordinatesMatrix.append(np.array(nodesLibrary[node]))
            nodeNumbers.append(node - 1)
        [[Xi, Yi, Zi], [Xj, Yj, Zj], [Xk, Yk, Zk], [Xl, Yl, Zl]] = coordinatesMatrix
        [number_i, number_j, number_k, number_l] = nodeNumbers

        # matrix = [[1, Xi, Yi, Zi], [1, Xj, Yj, Zj], [1, Xk, Yk, Zk], [1, Xl, Yl, Zl]]
        # volume = np.abs(np.linalg.det(matrix)) / 6
        volume = np.abs(np.linalg.det([[Xj - Xi, Yj - Yi, Zj - Zi], [Xk - Xi, Yk - Yi, Zk - Zi], [Xl - Xi, Yl - Yi, Zl - Zi]]))

        localHeatCapcitnceMatrix = 1/20 * density * specificHeat * volume * localMatrix
        globalHeatCapcitnceMatrix = getGlobalMatrix3D(globalHeatCapcitnceMatrix, localHeatCapcitnceMatrix, number_i, number_j, number_k, number_l)

    return globalHeatCapcitnceMatrix



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

        #######
        Bi = Yj - Yk
        Bj = Yk - Yi
        Bk = Yi - Yj
        Ci = Xk - Xj
        Cj = Xi - Xk
        Ck = Xj - Xi

        gradientMatrix = [[Bi, Bj, Bk], [Ci, Cj, Ck]]

        J = np.abs(np.linalg.det(np.dot(gradientMatrix, coordinatesMatrix)))

        #######

        area = 0.5 * abs(Xi * (Yj - Yk) + Xj * (Yk - Yi) + Xk * (Yi - Yj))

        localHeatCapcitnceMatrix = 1/12 * density * specificHeat * area * localMatrix * J
        globalHeatCapcitnceMatrix = getGlobalMatrix(globalHeatCapcitnceMatrix, localHeatCapcitnceMatrix, number_i, number_j, number_k)

    return globalHeatCapcitnceMatrix