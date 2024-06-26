import numpy as np
import numpy.linalg as la

from readingMesh import readingMesh
from readingMaterialProperties import getConductivity, getDensity, getSpecificHeat
from getGlobalMatrix import getGlobalMatrix3D
from applyBC import nullMatrixRow, applyBCtoF, nullMatrixCol

fileName = "../fixtures/3-05_static_3D.inp"
[elementsLibrary, nodesLibrary] = readingMesh(fileName)

conductivity = getConductivity(fileName)
density = getDensity(fileName)
specificHeat = getSpecificHeat(fileName)


# матрица теплопроводности

# globalCondictivityMatrix = np.zeros([len(nodesLibrary), len(nodesLibrary)])
# materialPropertiesMatrix = [[conductivity, 0, 0], [0, conductivity, 0], [0, 0, conductivity]]

# for number in range(1, len(elementsLibrary) + 1):

#     coordinatesMatrix = []
#     nodeNumbers = []

#     for node in elementsLibrary[number]:
#         coordinatesMatrix.append(np.array(nodesLibrary[node]))
#         nodeNumbers.append(node - 1)
#     [[Xi, Yi, Zi], [Xj, Yj, Zj], [Xk, Yk, Zk], [Xl, Yl, Zl]] = coordinatesMatrix
#     [number_i, number_j, number_k, number_l] = nodeNumbers

#     matrix = [[1, Xi, Yi, Zi], [1, Xj, Yj, Zj], [1, Xk, Yk, Zk], [1, Xl, Yl, Zl]]
#     invMatrix = np.linalg.inv(matrix)

#     volume = np.abs(np.linalg.det([[Xj - Xi, Yj - Yi, Zj - Zi], [Xk - Xi, Yk - Yi, Zk - Zi], [Xl - Xi, Yl - Yi, Zl - Zi]]))
#     gradientMatrix = np.array(invMatrix[1 : len(invMatrix) + 1])

#     localCondictivityMatrix = volume * np.dot(np.dot(np.transpose(gradientMatrix), materialPropertiesMatrix), gradientMatrix) 
#     globalCondictivityMatrix = getGlobalMatrix3D(globalCondictivityMatrix, localCondictivityMatrix, number_i, number_j, number_k, number_l)


globalCondictivityMatrix = np.zeros([len(nodesLibrary), len(nodesLibrary)])
Be = [[-1, 1, 0, 0], [-1, 0, 1, 0], [-1, 0, 0, 1]]

for number in range(1, len(elementsLibrary) + 1):

    coordinatesMatrix = []
    nodeNumbers = []

    for node in elementsLibrary[number]:
        coordinatesMatrix.append(np.array(nodesLibrary[node]))
        nodeNumbers.append(node - 1)
    [[Xi, Yi, Zi], [Xj, Yj, Zj], [Xk, Yk, Zk], [Xl, Yl, Zl]] = coordinatesMatrix
    [number_i, number_j, number_k, number_l] = nodeNumbers

    j = np.dot(Be, coordinatesMatrix)
    jDet = np.abs(np.linalg.det(j))
    jInv = np.linalg.inv(j)
    
    gradientMatrix = np.dot(jInv, Be)

    localCondictivityMatrix = 0.25 * jDet * conductivity * np.dot(np.transpose(gradientMatrix), gradientMatrix) 
    globalCondictivityMatrix = getGlobalMatrix3D(globalCondictivityMatrix, localCondictivityMatrix, number_i, number_j, number_k, number_l)


# вектор сил и НУ

force = np.zeros(len(nodesLibrary))
initialT = np.zeros(len(force))


# ГУ

set1 = [1,   2,   3,   4,   9,  10,  11,  12,  13,  14,  15,  16,  17,  18,  19,  20,
  21,  22,  23,  24,  25,  26,  27,  28,  29,  30,  31,  32,  33,  34,  35,  36,
  37,  38,  39,  40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,
  53,  54,  55,  56,  57,  58,  59,  60,  61,  62,  63,  64,  65,  66,  67,  68,
  69,  70,  71,  72,  73,  74,  75,  76,  77,  78,  79,  80,  81,  82,  83,  84,
  85,  86,  87,  88,  89,  90,  91,  92,  93,  94,  95,  96,  97,  98,  99, 100,
 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116,
 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 375, 376, 377, 378,
 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394,
 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410,
 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426,
 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442,
 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458,
 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474,
 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490,
 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506,
 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522,
 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538,
 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554,
 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570,
 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586,
 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598]

set2 = [2,    3,    5,    6,    7,    8,   65,   66,   67,   68,  129,  130,  131,  132,  133,  134,
  135,  136,  137,  138,  139,  140,  141,  142,  143,  144,  145,  146,  147,  148,  149,  150,
  151,  152,  153,  154,  155,  156,  157,  158,  159,  160,  161,  162,  163,  164,  165,  166,
  167,  168,  169,  170,  171,  172,  173,  174,  175,  176,  177,  178,  179,  180,  181,  182,
  183,  184,  185,  186,  187,  188,  189,  190,  191,  192,  193,  194,  195,  196,  197,  198,
  199,  200,  201,  202,  203,  304,  305,  306,  307,  308,  309,  310,  311,  312,  313,  314,
  315,  316,  317,  318,  319,  320,  321,  322,  323,  324,  325,  326,  327,  328,  329,  330,
  331,  332,  333,  334,  335,  336,  337,  338,  339,  340,  341,  342,  343,  344,  345,  346,
  347,  348,  349,  350,  351,  352,  353,  354,  355,  356,  357,  358,  359,  360,  361,  362,
  363,  364,  365,  366,  367,  368,  369,  370,  371,  372,  373,  374,  599,  600,  601,  602,
  603,  604,  605,  606, 3284, 3285, 3286, 3287, 3288, 3289, 3290, 3291, 3292, 3293, 3294, 3295,
 3296, 3297, 3298, 3299, 3300, 3301, 3302, 3303, 3304, 3305, 3306, 3307, 3308, 3309, 3310, 3311,
 3312, 3313, 3314, 3315, 3316, 3317, 3318, 3319, 3320, 3321, 3322, 3323, 3324, 3325, 3326, 3327,
 3328, 3329, 3330, 3331, 3332, 3333, 3334, 3335, 3336, 3337, 3338, 3339, 3340, 3341, 3342, 3343,
 3344, 3345, 3346, 3347, 3348, 3349, 3350, 3351, 3352, 3353, 3354, 3355, 3356, 3357, 3358, 3359,
 3360, 3361, 3362, 3363, 3364, 3365, 3366, 3367, 3368, 3369, 3370, 3371, 3372, 3373, 3374, 3375,
 3376, 3377, 3378, 3379, 3380, 3381, 3382, 3383, 3384, 3385, 3386, 3387, 3388, 3389, 3390, 3391,
 3392, 3393, 3394, 3395, 3396, 3397, 3398, 3399, 3400, 3401, 3402, 3403, 3404, 3405, 3406, 3407,
 3408, 3409, 3410, 3411, 3412, 3413, 3414, 3415, 3416, 3417, 3418, 3419, 3420, 3421, 3422, 3423,
 3424, 3425, 3426, 3427, 3428, 3429, 3430, 3431, 3432, 3433, 3434, 3435, 3436, 3437, 3438, 3439,
 3440, 3441, 3442, 3443, 3444, 3445, 3446, 3447, 3448, 3449, 3450, 3451, 3452, 3453, 3454, 3455,
 3456, 3457, 3458, 3459, 3460, 3461, 3462, 3463, 3464, 3465, 3466, 3467, 3468, 3469, 3470, 3471,
 3472, 3473, 3474, 3475, 3476, 3477, 3478, 3479, 3480, 3481, 3482, 3483, 3484, 3485, 3486, 3487,
 3488, 3489, 3490, 3491, 3492, 3493, 3494, 3495, 3496, 3497, 3498, 3499, 3500, 3501, 3502, 3503,
 3504, 3505, 3506, 3507, 3508, 3509, 3510, 3511, 3512, 3513, 3514, 3515, 3516, 3517, 3518, 3519,
 3520, 3521, 3522, 3523, 3524, 3525, 3526, 3527, 3528, 3529, 3530, 3531, 3532, 3533, 3534, 3535,
 3536, 3537, 3538, 3539, 3540, 3541, 3542, 3543, 3544, 3545, 3546, 3547, 3548, 3549, 3550, 3551]

# BC = { 5.0: set1, 20.0: set2 }
BC = { 20.0: set2, 5.0: set1 }


# стационарное решение

matrixK = nullMatrixRow(globalCondictivityMatrix, BC)
newForce = applyBCtoF(matrixK, force, BC)
newConductivityMatrix = nullMatrixCol(matrixK, BC)

temperature = la.solve(newConductivityMatrix, newForce)

for i in temperature:
    print(i)