# coding: utf-8

from deworld.layers import LAYER_TYPE

class BasePoint(object):

    def __init__(self, layer_type, name, x, y, power, default_power=0.0):
        self.layer_type = layer_type
        self.name = name
        self.x = x
        self.y = y
        self.power = power if callable(power) else lambda world, x, y: power
        self._powers = None
        self.default_power = default_power

    def update_world(self, world):
        if self.layer_type == LAYER_TYPE.HEIGHT:
            self.update_powers(world.layer_height, world)
        elif self.layer_type == LAYER_TYPE.TEMPERATURE:
            self.update_powers(world.layer_temperature, world)
        elif self.layer_type == LAYER_TYPE.WETNESS:
            self.update_powers(world.layer_wetness, world)
        elif self.layer_type == LAYER_TYPE.VEGETATION:
            self.update_powers(world.layer_vegetation, world)

    def update_powers(self, layer, world):
        pass

    def _get_powers_rect(self, w, h):
        powers = []
        for i in xrange(h):
            powers.append([self.default_power]*w)
        return powers
