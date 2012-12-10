# coding: utf-8

from deworld.utils import copy2d
from deworld.exceptions import DeworldException


class BaseLayer(object):

    def __init__(self, world, default=0.0, default_power=None, data=None):

        if default_power is None:
            default_power = default

        self.world = world

        self.base_data = []
        for y in xrange(0, self.h):
            self.base_data.append([default] * self.w)
        self.data = copy2d(self.base_data) if data is None else data
        self.next_data = copy2d(self.base_data)

        self.power = []
        for y in xrange(0, self.h):
            self.power.append([default_power] * self.w)

    def serialize(self):
        return {'data': self.data}

    @classmethod
    def deserialize(cls, world, data):
        raise DeworldException('deserialize method not implemented for layer %r' % cls)

    def __eq__(self, other):
        return ( self.__class__ is other.__class__ and
                 self.data == other.data )

    @property
    def w(self): return self.world.w

    @property
    def h(self): return self.world.h

    @property
    def config(self): return self.world.config

    def _merge_config(self, config):
        for arg_name, arg_value in config.__dict__.items():
            if arg_name.isupper():
                setattr(self, arg_name, arg_value)

    def add_power(self, x, y, power):
        self.power[y][x] += power

    def apply_powers(self, x, y, powers):

        for i, row in enumerate(powers):
            if y+i < 0 or self.h <= y+i : continue

            for j, power in enumerate(row):
                if x+j < 0 or self.w <= x+j : continue

                self.add_power(x+j, y+i, power)

    def sync(self):
        pass

    def apply(self):
        self.data = copy2d(self.next_data)
