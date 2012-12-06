# coding: utf-8


def copy2d(original):
    data = [None] * len(original)
    for i, row in enumerate(original):
        data[i] = row[:]
    return data
