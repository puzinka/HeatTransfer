import numpy as np
from getGlobalMatrix import getGlobalMatrix

# def getConductivityMatrix(elementsLibrary, nodesLibrary, conductivity):

#     globalCondictivityMatrix = np.zeros([len(nodesLibrary), len(nodesLibrary)])

#     for number in range(1, len(elementsLibrary) + 1):
#         a = 1

#     return elementsLibrary[1][1]


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





# def getConductivityMatrix(elementsLibrary, nodesLibrary, conductivity):

#     #линейный треугольный элемент

#     globalCondictivityMatrix = np.zeros([len(nodesLibrary), len(nodesLibrary)])

#     dN = [[-1, 1, 0], [-1, 0, 1]]

#     for number in range(1, len(elementsLibrary) + 1):

#         coordinatesMatrix = []
#         nodeNumbers = []

#         for node in elementsLibrary[number]:
#             coordinatesMatrix.append(np.array(nodesLibrary[node]))
#             nodeNumbers.append(node - 1)

#         [number_i, number_j, number_k] = nodeNumbers
#         [[Xi, Yi], [Xj, Yj], [Xk, Yk]] = coordinatesMatrix

#         Jacobian = np.dot(dN, coordinatesMatrix)
#         invJacobian = np.linalg.inv(Jacobian)

#         # area = 0.5 * abs(Xi * (Yj - Yk) + Xj * (Yk - Yi) + Xk * (Yi - Yj))

#         a = np.dot(invJacobian, dN)
#         b = np.dot(np.transpose(a), a)
#         # localCondictivityMatrix = area * conductivity * b
#         localCondictivityMatrix = 0.5 * np.linalg.norm(Jacobian) * conductivity * b

#         globalCondictivityMatrix = getGlobalMatrix(globalCondictivityMatrix, localCondictivityMatrix, number_i, number_j, number_k)

#     return globalCondictivityMatrix




# def getConductivityMatrix(elementsLibrary, nodesLibrary, conductivity):

#     #линейный треугольный элемент

#     globalCondictivityMatrix = np.zeros([len(nodesLibrary), len(nodesLibrary)])

#     dN = [[-1, 1, 0], [-1, 0, 1]]

#     for number in range(1, len(elementsLibrary) + 1):

#         coordinatesMatrix = []
#         nodeNumbers = []

#         for node in elementsLibrary[number]:
#             coordinatesMatrix.append(np.array(nodesLibrary[node]))
#             nodeNumbers.append(node - 1)

#         [number_i, number_j, number_k] = nodeNumbers
#         [[Xi, Yi], [Xj, Yj], [Xk, Yk]] = coordinatesMatrix

#         Jacobian = np.dot(dN, coordinatesMatrix)
#         invJacobian = np.linalg.inv(Jacobian)

#         # area = 0.5 * abs(Xi * (Yj - Yk) + Xj * (Yk - Yi) + Xk * (Yi - Yj))

#         a = np.dot(invJacobian, dN)
#         b = np.dot(np.transpose(a), a)

#         c = np.dot(np.transpose(dN), dN)

#         # localCondictivityMatrix = area * conductivity * b
#         localCondictivityMatrix = 0.5 * np.linalg.norm(Jacobian) * conductivity * c

#         globalCondictivityMatrix = getGlobalMatrix(globalCondictivityMatrix, localCondictivityMatrix, number_i, number_j, number_k)

#     return globalCondictivityMatrix