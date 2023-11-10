import numpy as np

# сборка глобальной матрицы

def getGlobalMatrix(globalMatrix, localMatrix, numberNode_i, numberNode_j, numberNode_k):

    globalMatrix[numberNode_i, numberNode_i] += localMatrix[0, 0]
    globalMatrix[numberNode_j, numberNode_j] += localMatrix[1, 1]
    globalMatrix[numberNode_k, numberNode_k] += localMatrix[2, 2]

    globalMatrix[numberNode_i, numberNode_j] += localMatrix[0, 1]
    globalMatrix[numberNode_j, numberNode_i] += localMatrix[1, 0]

    globalMatrix[numberNode_i, numberNode_k] += localMatrix[0, 2]
    globalMatrix[numberNode_k, numberNode_i] += localMatrix[2, 0]

    globalMatrix[numberNode_j, numberNode_k] += localMatrix[1, 2]
    globalMatrix[numberNode_k, numberNode_j] += localMatrix[2, 1]

    return globalMatrix