# coding: utf-8

from deworld.layers import LAYER_TYPE

from deworld.layers import BaseLayer
import collections

class LogLayer(BaseLayer):

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.value = None

    def add_power(self, x ,y, power):
        if x == self.x and y == self.y:
            self.value = power


class BasePoint(object):

    def __init__(self, layer_type, name, x, y, power, default_power=0.0):
        self.layer_type = layer_type
        self.name = name
        self.x = x
        self.y = y
        self.power = power if isinstance(power, collections.abc.Callable) else lambda world, x, y: power
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
        elif self.layer_type == LAYER_TYPE.SOIL:
            self.update_powers(world.layer_soil, world)

    def log_powers_for(self, world, x, y):
        logger = LogLayer(world, x, y)
        self.update_powers(logger, world)
        return logger.value

    def update_powers(self, layer, world):
        pass

    def _get_powers_rect(self, w, h):
        powers = []
        for i in range(h):
            powers.append([self.default_power]*w)
        return powers
