
def zeros(shape):

    if len(shape) == 0:
        raise ValueError("Необходимо указать форму массива")

    if len(shape) == 1:
        return [0] * shape[0]
    else:
        return [zeros(shape[1:]) for _ in range(shape[0])]
        