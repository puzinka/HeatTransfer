
# применение ГУ

def nullMatrixRow(matrix, BC):

    for temperature in BC:
        for node in BC[temperature]:
            length = len(matrix)

            for i in range(0, length):
                if i !=  (int(node) - 1):
                    matrix[int(node) - 1][i] = 0

    return matrix

def applyBCtoF(matrix, force, BC):
    
    for temperature in BC:
        for node in BC[temperature]:
            force[int(node) - 1] = matrix[int(node) - 1][int(node) - 1] * temperature
    
    for temperature in BC:
        for node in BC[temperature]:
            length = len(force)

            for i in range(0, length):
                if i != (int(node) - 1):
                    force[i] -= matrix[i][int(node) - 1] * temperature
                    
    return force

def nullMatrixCol(matrix, BC, flag=False):
    
    for temperature in BC:
        for node in BC[temperature]:
            length = len(matrix)

            for i in range(0, length):
                if i !=  (int(node) - 1):
                    matrix[i][int(node) - 1] = 0

    return matrix

    