# применение ГУ

def applyBCtoMatrix(matrix, BC):

    for temperature in BC:
        for node in BC[temperature]:
            matrix[node - 1][0 :] = 0
            matrix[0 :][node - 1] = 0
            matrix[node - 1][node - 1] = 1
    
    return matrix

def applyBCtoVector(thermalForce, BC):

    for temperature in BC:
        for node in BC[temperature]:
            thermalForce[node - 1] = temperature
    
    return thermalForce


    