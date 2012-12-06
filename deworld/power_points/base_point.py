# coding: utf-8

from deworld.layers import LAYER_TYPE

class BasePoint(object):

    def __init__(self, layer_type, name, x, y, power):
        self.layer_type = layer_type
        self.name = name
        self.x = x
        self.y = y
        self.power = power
        self._powers = None

    def update_world(self, world):
        if self.layer_type == LAYER_TYPE.HEIGHT:
            self.update_powers(world.layer_height, world)
        elif self.layer_type == LAYER_TYPE.TEMPERATURE:
            self.update_powers(world.layer_temperature, world)

    def update_powers(self, layer, world):
        pass

    def _get_powers_rect(self, w, h):
        powers = []
        for i in xrange(h):
            powers.append([0]*w)
        return powers
