# coding: utf-8

linear = lambda power, normalized_distance: power*(1-normalized_distance)
equal = lambda power, normalized_distance: power
linear_2 = lambda power, normalized_distance: (power[0]*(1-normalized_distance), power[1]*(1-normalized_distance))
