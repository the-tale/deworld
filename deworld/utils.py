# coding: utf-8

E = 0.00001

def copy2d(original):
    data = [None] * len(original)
    for i, row in enumerate(original):
        data[i] = row[:]
    return data


def resize2d(array, new_w, new_h):
    w = len(array[0])
    h = len(array)

    result = []

    if w > new_w:
        result = [row[:new_w] for row in array]
    elif w < new_w:
        result = [row + [row[-1]]*(new_w-w) for row in array]
    else:
        result = copy2d(array)

    if h > new_h:
        result = result[:new_h]

    if h < new_h:
        result = result + [result[-1]]*(new_h-h)

    return result

def shift2d(array, dx, dy):

    result = copy2d(array)

    for x in range(dx):
        for row in result:
            row.insert(0, row.pop())

    for y in range(dy):
        result.insert(0, result.pop())

    return result

def prepair_to_approximation(points, default=None):
    '''
    points = [(distance or power, some value)]

    do linear approximation:

      find max distance and define it as Q
      then other distance will be Kn*Q
      so, KQ - is an impact of point to result value
    '''
    if not points:
        return [(1.0, default)]

    for distance, point in points:
        if -E < distance < E:
            return [(1.0, point)]

    max_distance = float(max(p[0] for p in points))
    SK = sum(max_distance/p[0] for p in points)

    Q = 1.0 / SK

    return [(Q * max_distance/p[0], p[1]) for p in points]
