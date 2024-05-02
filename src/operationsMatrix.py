import numpy as np

# from convertToDecimal import convertToDecimal, convertToDecimalVector
from zerosArray import zeros

def sumVectors(A, B):

    C = zeros([len(A)])

    if len(A) != len(B):
        raise Exception("len(A) != len(B)")

    for i in range(len(A)):
        C[i] = A[i] + B[i]
    

    return C

def subVectors(A, B):

    C = zeros([len(A)])

    if len(A) != len(B):
        raise Exception("len(A) != len(B)")

    for i in range(len(A)):
        C[i] = A[i] - B[i]

    return C

def multiplyMatrixToMatrix(A, B):

    # A = convertToDecimal(A1)
    # B = convertToDecimal(B1)

    n = len(A)
    m = len(A[0])
    t = len(B)
    p = len(B[0])

    if m != t:
        raise Exception("len(A[0]) != len(B)")

    C = zeros([n, p])

    for i in range (n):
        for j in range(p):
            for k in range(m):
                C[i][j] += A[i][k] * B[k][j]


    return C

def multiplyMatrixToVector(A, B):

    # A = convertToDecimal(A1)
    # B = convertToDecimalVector(B1)

    n = len(A)
    m = len(A[0])
    t = len(B)

    if m != t:
       raise Exception("len(A[0]) != len(B)")

    C = zeros([n])

    for i in range(n):
        for j in range(m):

            # if A[i][j] == float('inf'):
            #     print(A)
            #     raise Exception("A is inf")

            # if B[j] == float('inf'):
            #     print(B)
            #     raise Exception("B is inf")
            
            # try:
            C[i] += A[i][j] * B[j] 
            # except:
            #     print(f'A ${A}')
            #     print(f'B ${B}')
            #     exit()

    return C

def multiplyNumberToVector(number, A):

    # A = convertToDecimal(A1)
    # B = convertToDecimalVector(B1)

    n = len(A)
    C = zeros([n])

    for i in range(n):
        C[i] += A[i] * number

    return C
