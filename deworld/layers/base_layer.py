# coding: utf-8

from deworld.utils import copy2d


class BaseLayer(object):

    MAX = 100

    def __init__(self, world, w, h, default=0.0):
        self.world = world
        self.w = w
        self.h = h

        self.base_data = []
        for y in xrange(0, h):
            self.base_data.append([default] * w)
        self.data = copy2d(self.base_data)
        self.power = copy2d(self.base_data)
        self.next_data = copy2d(self.base_data)

    def get_normalized_data(self):
        data = copy2d(self.base_data)
        for y in xrange(self.h):
            for x in xrange(self.w):
                data[y][x] = self.data[y][x] / float(self.MAX)
        return data

    def add_power(self, x, y, power):
        self.power[y][x] += power

    def apply_powers(self, x, y, powers):

        for i, row in enumerate(powers):
            if y+i < 0 or self.h <= y+i : continue

            for j, power in enumerate(row):
                if x+j < 0 or self.w <= x+j : continue

                self.add_power(x+j, y+i, power)

    def sync(self):
        # power on base of last step data and current power
        pass

    def apply(self):
        self.data = copy2d(self.next_data)
