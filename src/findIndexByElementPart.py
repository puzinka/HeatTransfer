###### функция, которая ищет индекс элемента со значением "*Element" ######

def findIndexByElementPart(array, elementPart):
    newArray = []
    for element in array:
        if (element.find(elementPart) != -1):
            return array.index(element)
    raise Exception('Element does not exist')
    