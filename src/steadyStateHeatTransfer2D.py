import numpy as np
import numpy.linalg as la

from readingMesh import readingMesh
from readingMaterialProperties import getConductivity
from getGlobalMatrix import getGlobalMatrix
from applyBC import nullMatrixRow, applyBCtoF, nullMatrixCol
from plotting2D import plotting2D


fileName = "../fixtures/3-05_static_2D.inp"
[elementsLibrary, nodesLibrary] = readingMesh(fileName)

conductivity = getConductivity(fileName)


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

    area = 0.5 * abs(Xi * (Yj - Yk) + Xj * (Yk - Yi) + Xk * (Yi - Yj))

    matrix = [[1, Xi, Yi], [1, Xj, Yj], [1, Xk, Yk]]
    invMatrix = np.linalg.inv(matrix)
    gradientMatrix = np.array(invMatrix[1 : len(invMatrix) + 1])

    [number_i, number_j, number_k] = nodeNumbers

    # localCondictivityMatrix = 0.25 / area * np.dot(np.dot(np.transpose(gradientMatrix), materialPropertiesMatrix), gradientMatrix)
    localCondictivityMatrix = area * np.dot(np.dot(np.transpose(gradientMatrix), materialPropertiesMatrix), gradientMatrix)

    globalCondictivityMatrix = getGlobalMatrix(globalCondictivityMatrix, localCondictivityMatrix, number_i, number_j, number_k)


# вектор сил

force = np.zeros(len(nodesLibrary))


# ГУ

set1 = [3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,  14,  15,  16,  17,  18,
  19,  20,  21,  22,  23,  24,  25,  26,  27,  28,  29,  30,  31,  32,  33,  34,
  35, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600,
 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616,
 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629]

set2 = [1,   2,   3,  69,  70,  71,  72,  73,  74,  75,  76,  77,  78,  79,  80,  81,
  82,  83,  84,  85,  86,  87,  88,  89,  90,  91,  92,  93,  94,  95,  96,  97,
  98,  99, 100, 101, 102, 103, 104, 105, 106, 107, 583, 584, 585, 666, 667, 668,
 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684,
 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700,
 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716,
 717]

# BC = { 5.0: set1, 20.0: set2 }
BC = { 20.0: set2, 5.0: set1 }


# стационарное решение

matrixK = nullMatrixRow(globalCondictivityMatrix, BC)
newForce = applyBCtoF(matrixK, force, BC)
newConductivityMatrix = nullMatrixCol(matrixK, BC)

temperature = la.solve(newConductivityMatrix, newForce)

for i in temperature:
    print(i)

# plotting2D(elementsLibrary, nodesLibrary, temperature)
