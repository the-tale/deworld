# coding: utf-8

E = 0.00001

def copy2d(original):
    data = [None] * len(original)
    for i, row in enumerate(original):
        data[i] = row[:]
    return data


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
