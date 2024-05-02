import numpy as np
import random
from getGlobalMatrix import getGlobalMatrix, getGlobalMatrix3D

from convertToDecimal import convertToDecimalMatrix, convertToDecimalNumber


def getConductivityMatrix3D(elementsLibrary, nodesLibrary, conductivity):

    # globalCondictivityMatrix = np.zeros([len(nodesLibrary), len(nodesLibrary)])
    # materialPropertiesMatrix = [[conductivity, 0, 0], [0, conductivity, 0], [0, 0, conductivity]]
    # gradientMatrix = (1/6) * np.array([[0, -3, 3, 0], [3, -1, -1, -1], [0, -1, -1, 2]])

    # for number in range(1, len(elementsLibrary) + 1):

    #         coordinatesMatrix = []
    #         nodeNumbers = []

    #         for node in elementsLibrary[number]:
    #             coordinatesMatrix.append(np.array(nodesLibrary[node]))
    #             nodeNumbers.append(node - 1)
    #         [[Xi, Yi, Zi], [Xj, Yj, Zj], [Xk, Yk, Zk], [Xl, Yl, Zl]] = coordinatesMatrix
    #         [number_i, number_j, number_k, number_l] = nodeNumbers

    #         matrix = [[1, Xi, Yi, Zi], [1, Xj, Yj, Zj], [1, Xk, Yk, Zk], [1, Xl, Yl, Zl]]
    #         volume = np.abs(np.linalg.det(matrix)) / 6

    #         localCondictivityMatrix = volume * np.dot(np.dot(np.transpose(gradientMatrix), materialPropertiesMatrix), gradientMatrix)

    #         globalCondictivityMatrix = getGlobalMatrix3D(globalCondictivityMatrix, localCondictivityMatrix, number_i, number_j, number_k, number_l)


    globalCondictivityMatrix = np.zeros([len(nodesLibrary), len(nodesLibrary)])
    materialPropertiesMatrix = [[conductivity, 0, 0], [0, conductivity, 0], [0, 0, conductivity]]

    for number in range(1, len(elementsLibrary) + 1):

            coordinatesMatrix = []
            nodeNumbers = []

            for node in elementsLibrary[number]:
                coordinatesMatrix.append(np.array(nodesLibrary[node]))
                nodeNumbers.append(node - 1)
            [[Xi, Yi, Zi], [Xj, Yj, Zj], [Xk, Yk, Zk], [Xl, Yl, Zl]] = coordinatesMatrix
            [number_i, number_j, number_k, number_l] = nodeNumbers

            matrix = [[1, Xi, Yi, Zi], [1, Xj, Yj, Zj], [1, Xk, Yk, Zk], [1, Xl, Yl, Zl]]
            invMatrix = np.linalg.inv(matrix)

            volume = np.abs(np.linalg.det([[Xj - Xi, Yj - Yi, Zj - Zi], [Xk - Xi, Yk - Yi, Zk - Zi], [Xl - Xi, Yl - Yi, Zl - Zi]]))
            # volume = np.abs(np.linalg.det(matrix)) / 6

            # gradientMatrix = (1 / (6 * volume)) * np.array(invMatrix.slice(1, len(invMatrix) + 1))
            gradientMatrix = np.array(invMatrix[1 : len(invMatrix) + 1])

            localCondictivityMatrix = volume * np.dot(np.dot(np.transpose(gradientMatrix), materialPropertiesMatrix), gradientMatrix) 
            globalCondictivityMatrix = getGlobalMatrix3D(globalCondictivityMatrix, localCondictivityMatrix, number_i, number_j, number_k, number_l)

    return globalCondictivityMatrix



def getConductivityMatrixOld(elementsLibrary, nodesLibrary, conductivity, flag = False):

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

        #######

        J = np.abs(np.linalg.det(np.dot(gradientMatrix, coordinatesMatrix)))

        #######

        [number_i, number_j, number_k] = nodeNumbers


        localCondictivityMatrix = 0.25 * area * np.dot(np.dot(np.transpose(gradientMatrix), materialPropertiesMatrix), gradientMatrix)

        globalCondictivityMatrix = getGlobalMatrix(globalCondictivityMatrix, localCondictivityMatrix, number_i, number_j, number_k)

    return globalCondictivityMatrix




def getConductivityMatrix(elementsLibrary, nodesLibrary, conductivity, flag = False):

    # globalCondictivityMatrix = np.zeros([len(nodesLibrary), len(nodesLibrary)])
    # materialPropertiesMatrix = [[conductivity, 0], [0, conductivity]]

    # for number in range(1, len(elementsLibrary) + 1):

    #     coordinatesMatrix = []
    #     nodeNumbers = []

    #     for node in elementsLibrary[number]:
    #         coordinatesMatrix.append(np.array(nodesLibrary[node]))
    #         nodeNumbers.append(node - 1)
    #     [[Xi, Yi], [Xj, Yj], [Xk, Yk]] = coordinatesMatrix

    #     area = 0.5 * abs(Xi * (Yj - Yk) + Xj * (Yk - Yi) + Xk * (Yi - Yj))

    #     Bi = Yj - Yk
    #     Bj = Yk - Yi
    #     Bk = Yi - Yj
    #     Ci = Xk - Xj
    #     Cj = Xi - Xk
    #     Ck = Xj - Xi

    #     gradientMatrix = [[Bi, Bj, Bk], [Ci, Cj, Ck]]

    #     [number_i, number_j, number_k] = nodeNumbers

    #     localCondictivityMatrix = 0.25 * area * np.dot(np.dot(np.transpose(gradientMatrix), materialPropertiesMatrix), gradientMatrix)

    #     globalCondictivityMatrix = getGlobalMatrix(globalCondictivityMatrix, localCondictivityMatrix, number_i, number_j, number_k)

    # return globalCondictivityMatrix

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

        matrix = [[1, Xi, Yi], [1, Xj, Yj], [1, Xk, Yk]]
        invMatrix = np.linalg.inv(matrix)
        gradientMatrix = np.array(invMatrix[1 : len(invMatrix) + 1])

        [number_i, number_j, number_k] = nodeNumbers


        localCondictivityMatrix = 0.25 * area * np.dot(np.dot(np.transpose(gradientMatrix), materialPropertiesMatrix), gradientMatrix)

        globalCondictivityMatrix = getGlobalMatrix(globalCondictivityMatrix, localCondictivityMatrix, number_i, number_j, number_k)

    return globalCondictivityMatrix


