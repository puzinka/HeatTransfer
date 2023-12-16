import numpy as np
from getGlobalMatrix import getGlobalMatrix

def getConductivityMatrix(elementsLibrary, nodesLibrary, conductivity):

    #линейный треугольный элемент

    globalCondictivityMatrix = np.zeros([len(nodesLibrary), len(nodesLibrary)])
    materialPropertiesMatrix = [[conductivity, 0], [0, conductivity]]

    for number in range(1, len(elementsLibrary) + 1):

        coordinatesMatrix = []
        nodeNumbers = []


        for node in elementsLibrary[number]:
            coordinatesMatrix.append(np.array(nodesLibrary[node]))
            nodeNumbers.append(node - 1)
        [[Xi, Yi], [Xj, Yj], [Xk, Yk]] = coordinatesMatrix

        area = 0.5 * abs(Xi * (Yj - Yk) + Xj * (Yk - Yi) + Xk * (Yi - Yj))

        Bi = Yj - Yk
        Bj = Yk - Yi
        Bk = Yi - Yj
        Ci = Xk - Xj
        Cj = Xi - Xk
        Ck = Xj - Xi

        gradientMatrix = [[Bi, Bj, Bk], [Ci, Cj, Ck]]

        [number_i, number_j, number_k] = nodeNumbers

        localCondictivityMatrix = 0.25 * area * np.dot(np.dot(np.transpose(gradientMatrix), materialPropertiesMatrix), gradientMatrix)

        globalCondictivityMatrix = getGlobalMatrix(globalCondictivityMatrix, localCondictivityMatrix, number_i, number_j, number_k)

    return globalCondictivityMatrix
