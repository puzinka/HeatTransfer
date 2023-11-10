# функция, которая ищет индекс элемента со значением "*Element" 

def findIndexByElementPart(array, elementPart):
    newArray = []
    for element in array:
        if (element.find(elementPart) != -1):
            return array.index(element)
    raise Exception('Element does not exist')
    
def findArrayOfIndexesByElementPart(array, elementPart):
    indexesArray = []
    count = 0
    for element in array:
        if (element.find(elementPart) != -1):
            count += 1
            index = array.index(element)
            indexesArray.append(index)

    if count == 0:
        raise Exception('Element does not exist')
    elif count == 1:
        return index
    else:
        return indexesArray

