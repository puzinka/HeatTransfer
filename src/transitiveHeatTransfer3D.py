import numpy as np
import numpy.linalg as la
import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve
from scipy.linalg import solve

from readingMesh import readingMesh
from readingMaterialProperties import getConductivity, getDensity, getSpecificHeat
from getGlobalMatrix import getGlobalMatrix3D
from applyBC import nullMatrixRow, applyBCtoF, nullMatrixCol


import csv

def write_2d_array_to_csv(array, filename):
  """
  Write a 2D array to a CSV file.

  Args:
    array: The 2D array to write to the CSV file.
    filename: The name of the CSV file to write to.
  """

  with open(filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')

    # Write each row of the array to the CSV file.
    for row in array:
      csvwriter.writerow(row)



fileName = "../fixtures/4-05_fixed_3D.inp"
# fileName = "../fixtures/.inp"

fileName = "../fixtures/8_05.inp"


[elementsLibrary, nodesLibrary] = readingMesh(fileName)

conductivity = getConductivity(fileName)
density = getDensity(fileName)
specificHeat = getSpecificHeat(fileName)
# density = 1000
# conductivity = 10
# specificHeat = 100


# матрица теплопроводности

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
    
    gradientMatrix = np.array(invMatrix[1 : len(invMatrix) + 1])

    localCondictivityMatrix = volume * np.dot(np.dot(np.transpose(gradientMatrix), materialPropertiesMatrix), gradientMatrix) 
    globalCondictivityMatrix = getGlobalMatrix3D(globalCondictivityMatrix, localCondictivityMatrix, number_i, number_j, number_k, number_l)


# globalCondictivityMatrix = np.zeros([len(nodesLibrary), len(nodesLibrary)])
# Be = [[-1, 1, 0, 0], [-1, 0, 1, 0], [-1, 0, 0, 1]]

# for number in range(1, len(elementsLibrary) + 1):

#     coordinatesMatrix = []
#     nodeNumbers = []

#     for node in elementsLibrary[number]:
#         coordinatesMatrix.append(np.array(nodesLibrary[node]))
#         nodeNumbers.append(node - 1)
#     [[Xi, Yi, Zi], [Xj, Yj, Zj], [Xk, Yk, Zk], [Xl, Yl, Zl]] = coordinatesMatrix
#     [number_i, number_j, number_k, number_l] = nodeNumbers

#     j = np.dot(Be, coordinatesMatrix)
#     jDet = np.abs(np.linalg.det(j))
#     jInv = np.linalg.inv(j)
    
#     gradientMatrix = np.dot(jInv, Be)

#     localCondictivityMatrix = 0.25 * jDet * conductivity * np.dot(np.transpose(gradientMatrix), gradientMatrix) 
#     globalCondictivityMatrix = getGlobalMatrix3D(globalCondictivityMatrix, localCondictivityMatrix, number_i, number_j, number_k, number_l)

# матрица теплоемкости

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

    matrix = [[1, Xi, Yi, Zi], [1, Xj, Yj, Zj], [1, Xk, Yk, Zk], [1, Xl, Yl, Zl]]
    # volume = np.abs(np.linalg.det(matrix)) / 6
    volume = np.abs(np.linalg.det([[Xj - Xi, Yj - Yi, Zj - Zi], [Xk - Xi, Yk - Yi, Zk - Zi], [Xl - Xi, Yl - Yi, Zl - Zi]]))

    localHeatCapcitnceMatrix = 1/20 * density * specificHeat * volume * localMatrix
    globalHeatCapcitnceMatrix = getGlobalMatrix3D(globalHeatCapcitnceMatrix, localHeatCapcitnceMatrix, number_i, number_j, number_k, number_l)


# globalHeatCapcitnceMatrix = np.zeros([len(nodesLibrary), len(nodesLibrary)])

# localMatrix = np.array([
#     [2, 1, 1, 1], 
#     [1, 2, 1, 1],
#     [1, 1, 2, 1],
#     [1, 1, 1, 2]
# ])

# for number in range(1, len(elementsLibrary) + 1):

#     coordinatesMatrix = []
#     nodeNumbers = []

#     for node in elementsLibrary[number]:
#         coordinatesMatrix.append(np.array(nodesLibrary[node]))
#         nodeNumbers.append(node - 1)
#     [[Xi, Yi, Zi], [Xj, Yj, Zj], [Xk, Yk, Zk], [Xl, Yl, Zl]] = coordinatesMatrix
#     [number_i, number_j, number_k, number_l] = nodeNumbers
    
#     j = np.dot(Be, coordinatesMatrix)
#     jDet = np.abs(np.linalg.det(j))
#     # jInv = np.linalg.inv(j)

#     localHeatCapcitnceMatrix = (1 / (120)) * jDet * density * specificHeat * localMatrix
#     globalHeatCapcitnceMatrix = getGlobalMatrix3D(globalHeatCapcitnceMatrix, localHeatCapcitnceMatrix, number_i, number_j, number_k, number_l)


# вектор сил и НУ

force = np.zeros(len(nodesLibrary))
initialT = np.zeros(len(force))


# ГУ

# set1 = [1,   4,   9,  10,  20,  21,  22,  23,  24,  25,  26,  66,  67,  68,  69,  70,
#   71,  72,  73,  74,  75,  76,  77,  78,  79,  80,  81,  82,  83,  84,  85,  86,
#  188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203,
#  204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219,
#  220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235,
#  236]

# set2 = [1,   2,   3,   4,   5,   6,   7,   8,  11,  12,  13,  14,  15,  16,  17,  18,
#   19,  20,  21,  22,  23,  24,  25,  26,  27,  28,  29,  30,  31,  32,  33,  34,
#   35,  36,  37,  38,  39,  40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,
#   51,  52,  53,  54,  55,  56,  57,  58,  94,  95,  96,  97,  98,  99, 100, 101,
#  102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117,
#  118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133,
#  134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149,
#  150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163]

set2 = [1,   2,   3,   4,   5,   6,   7,   8,  11,  12,  13,  14,  15,  16,  17,  18,
  19,  20,  21,  22,  23,  24,  25,  26,  27,  28,  29,  30,  31,  32,  33,  34,
  35,  36,  37,  38,  39,  40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,
  51,  52,  53,  54,  55,  56,  57,  58,  59,  60,  61,  62,  63,  64,  65,  66,
  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,  77,  78,  79,  80,  81,  82,
  83,  84,  85,  86,  87,  88, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163,
 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179,
 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195,
 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211,
 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227,
 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243,
 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259,
 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275,
 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291,
 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307,
 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323,
 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339,
 340, 341, 342]

set1 = [1,   4,   9,  10,  22,  23,  24,  25,  26,  27,  28,  29,  30,  98,  99, 100,
 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116,
 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132,
 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 445, 446, 447, 448,
 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464,
 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480,
 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496,
 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512,
 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528,
 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544,
 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560,
 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576,
 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592,
 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608,
 609, 610, 611, 612, 613, 614, 615]

BC = { 20.0: set2, 5.0: set1 }
# BC = { 20.0: set2, 5.0: set1 }


# нестационарное решение

temperatureMoments = []
temperatureMoments.append(initialT)

invC = np.linalg.inv(globalHeatCapcitnceMatrix)
timeStep = 1
stepNumber = 0

matrixK = nullMatrixRow(globalCondictivityMatrix, BC)
newForce = applyBCtoF(matrixK, force, BC)
newConductivityMatrix = nullMatrixCol(matrixK, BC)

# write_2d_array_to_csv(globalHeatCapcitnceMatrix, 'C.csv')
# write_2d_array_to_csv(invC, 'invC.csv')
# write_2d_array_to_csv(newConductivityMatrix, 'K.csv')
# write_2d_array_to_csv([newForce], 'F.csv')

C = globalHeatCapcitnceMatrix
K = newConductivityMatrix
F = newForce


for i in range(5):
    
    stepNumber += 1
    print(stepNumber)
    
    # matrixK = nullMatrixRow(globalCondictivityMatrix, BC)
    # newForce = applyBCtoF(matrixK, force, BC)
    # newConductivityMatrix = nullMatrixCol(matrixK, BC)
        
    A = newConductivityMatrix + (2 / timeStep) * globalHeatCapcitnceMatrix
    b = np.dot((2 / timeStep) * globalHeatCapcitnceMatrix - newConductivityMatrix, initialT) + newForce
              
    
    # A = np.dot(C, timeStep)
    # b = F - np.dot(K, initialT) + np.dot(np.dot(C, initialT), timeStep)
    
    
    T = np.linalg.solve(A, b)
    
    print(max(T))
    print(min(T))
    print('\n')
    
    # LU = solve(A, np.eye(A.shape[0]), check_finite=True)
    # T = solve(A, b, check_finite=True, LU=LU)
    
    # T = spsolve(csc_matrix(A), b)

    
    
    # T = initialT - timeStep * np.dot(np.dot(invC, newConductivityMatrix), initialT) + timeStep * np.dot(invC, newForce)
    
    # for temperature in BC:
    #     for node in BC[temperature]:
    #         T[int(node) - 1] = temperature
    
    temperatureMoments.append(T)

    initialT = T
    # initialT = np.zeros(len(force))

# for i in temperatureMoments[-1]:
#     print(i)