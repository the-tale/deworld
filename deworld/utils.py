# coding: utf-8

E = 0.00001

def copy2d(original):
    data = [None] * len(original)
    for i, row in enumerate(original):
        data[i] = row[:]
    return data
