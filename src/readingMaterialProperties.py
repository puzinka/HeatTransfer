# чтение свойств материала из inp

def getConductivity(fileName):

    # чтение теплопроводности для тела, состоящего из одного материала 

    file = open(fileName, 'r')
    lines = file.read().split('\n')

    indexConductivity = lines.index('*Conductivity') + 1
    conductivity = float(lines[indexConductivity].replace(',', ''))

    return conductivity

def getDensity(fileName):

    # чтение плотности для тела, состоящего из одного материала 

    file = open(fileName, 'r')
    lines = file.read().split('\n')

    indexDensity = lines.index('*Density') + 1
    density = float(lines[indexDensity].replace(',', ''))

    return density

def getSpecificHeat(fileName):

    # чтение теплоёмкости для тела, состоящего из одного материала 

    file = open(fileName, 'r')
    lines = file.read().split('\n')

    indexSpecificHeat = lines.index('*Specific Heat') + 1
    specificHeat = float(lines[indexSpecificHeat].replace(',', ''))

    return specificHeat