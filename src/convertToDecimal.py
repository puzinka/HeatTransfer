from decimal import Decimal, getcontext
from zerosArray import zeros

getcontext().prec = 100

def convertToDecimalMatrix(matrix):

    # getcontext().prec = 40
    newMatrix = zeros([len(matrix), len(matrix[0])])

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            newMatrix[i][j] = Decimal(float(matrix[i][j]))

    return newMatrix

def convertToDecimalVector(matrix):

    # getcontext().prec = 40
    newMatrix = zeros([len(matrix)])

    for i in range(len(matrix)):
        newMatrix[i] = Decimal(float(matrix[i]))

    return newMatrix

def convertToDecimalNumber(num):
    
    # getcontext().prec = 40
    
    return Decimal(num)

# def convertToDecimal(matrix):
#     decimalMatrix = [[Decimal(element) for element in row] for row in matrix]
#     return decimalMatrix