import numpy as np
import numpy.linalg as la

from readingMesh import readingMesh
from readingMaterialProperties import getConductivity, getDensity, getSpecificHeat
from getGlobalMatrix import getGlobalMatrix
from applyBC import nullMatrixRow, applyBCtoF, nullMatrixCol

from plotting2D import plotting2D


# fileName = "../fixtures/4-05_fixed_2D.inp"
fileName = "../fixtures/4-05_2D.inp"
[elementsLibrary, nodesLibrary] = readingMesh(fileName)

conductivity = getConductivity(fileName)
density = getDensity(fileName)
specificHeat = getSpecificHeat(fileName)


# матрица теплопроводности

globalCondictivityMatrix = np.zeros([len(nodesLibrary), len(nodesLibrary)])
materialPropertiesMatrix = [[conductivity, 0], [0, conductivity]]

for number in range(1, len(elementsLibrary) + 1):

    coordinatesMatrix = []
    nodeNumbers = []

    for node in elementsLibrary[number]:
        coordinatesMatrix.append(np.array(nodesLibrary[node]))
        nodeNumbers.append(node - 1)
    [[Xi, Yi], [Xj, Yj], [Xk, Yk]] = coordinatesMatrix
    [number_i, number_j, number_k] = nodeNumbers

    area = 0.5 * abs(Xi * (Yj - Yk) + Xj * (Yk - Yi) + Xk * (Yi - Yj))

    matrix = [[1, Xi, Yi], [1, Xj, Yj], [1, Xk, Yk]]
    invMatrix = np.linalg.inv(matrix)
    gradientMatrix = np.array(invMatrix[1 : len(invMatrix) + 1])
    
    localCondictivityMatrix = area * np.dot(np.dot(np.transpose(gradientMatrix), materialPropertiesMatrix), gradientMatrix)

    # Bi = Yj - Yk
    # Bj = Yk - Yi
    # Bk = Yi - Yj
    # Ci = Xk - Xj
    # Cj = Xi - Xk
    # Ck = Xj - Xi

    # gradientMatrix = [[Bi, Bj, Bk], [Ci, Cj, Ck]]

    # localCondictivityMatrix = (1 / (4 * area)) * np.dot(np.dot(np.transpose(gradientMatrix), materialPropertiesMatrix), gradientMatrix)

    globalCondictivityMatrix = getGlobalMatrix(globalCondictivityMatrix, localCondictivityMatrix, number_i, number_j, number_k)


# матрица теплоемкости

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


# вектор сил и НУ

force = np.zeros(len(nodesLibrary))
initialT = np.zeros(len(force))


# ГУ

set1 = [2,  5, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89]

set2 = [1,  3,  4,  5, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]

arrayBC = [
    {5.0: set1, 6.0: set2},
    {5.0: set1, 7.0: set2},
    {5.0: set1, 8.0: set2},
    {5.0: set1, 9.0: set2},
    {5.0: set1, 10.0: set2},
    {5.0: set1, 11.0: set2}
]

# BC = {
#     5.0: [2,  5, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89],
#     20.0: [1,  3,  4,  5, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]
# }


# нестационарное решение


## постоянные ГУ

# temperatureMoments = []
# temperatureMoments.append(initialT)

# invC = np.linalg.inv(globalHeatCapcitnceMatrix)
# timeStep = 1
# stepNumber = 0

# matrixK = nullMatrixRow(globalCondictivityMatrix, BC)
# newForce = applyBCtoF(matrixK, force, BC)
# newConductivityMatrix = nullMatrixCol(matrixK, BC)

# for i in range(10):

#     stepNumber += 1
#     print(stepNumber)

#     T = initialT - timeStep * np.dot(np.dot(invC, newConductivityMatrix), initialT) + timeStep * np.dot(invC, newForce)
    
#     # for temperature in BC:
#     #     for node in BC[temperature]:
#     #         T[int(node) - 1] = temperature
    
#     temperatureMoments.append(T)

#     initialT = T


## переменные ГУ

temperatureMoments = []
temperatureMoments.append(initialT)

invC = np.linalg.inv(globalHeatCapcitnceMatrix)
timeStep = 1
stepNumber = 0

for BC in arrayBC:

    stepNumber += 1
    print(stepNumber)

    matrixK = nullMatrixRow(globalCondictivityMatrix, BC)
    newForce = applyBCtoF(matrixK, force, BC)
    newConductivityMatrix = nullMatrixCol(matrixK, BC)

    T = initialT - timeStep * np.dot(np.dot(invC, newConductivityMatrix), initialT) + timeStep * np.dot(invC, newForce)
    
    for temperature in BC:
        for node in BC[temperature]:
            T[int(node) - 1] = temperature
    
    temperatureMoments.append(T)

    initialT = T


for i in temperatureMoments[-1]:
    print(i)

plotting2D(elementsLibrary, nodesLibrary, temperatureMoments[-1])






# import csv

# def write_2d_array_to_csv(array, filename):
#   """Записывает двумерный массив в CSV-файл.

#   Args:
#     array: Массив для записи.
#     filename: Имя выходного CSV-файла.
#   """

#   with open(filename, 'w', newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     for row in array:
#       csvwriter.writerow(row)


# write_2d_array_to_csv(newConductivityMatrix, "test.csv")
