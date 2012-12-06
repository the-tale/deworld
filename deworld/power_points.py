# coding: utf-8

#################################################
#
# Различия точек силы:
#
# - фигура распространения влияния
# - функция изменения влияния на фигуре
#
#################################################

import math
import collections

from world import LAYER_TYPE

class BasePowerPoint(object):

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


class CircleAreaPoint(BasePowerPoint):

    def __init__(self, radius, normalizer, **kwargs):
        super(CircleAreaPoint, self).__init__(**kwargs)
        self.radius = radius
        self.normalizer = normalizer

    def update_powers(self, layer, world):

        w = h = 1+self.radius*2

        if self._powers is None:
            self._powers = self._get_powers_rect(w=w, h=h)
        else:
            layer.apply_powers(self.x-self.radius, self.y-self.radius, self._powers)
            return

        powers = self._powers

        for y in xrange(h):
            for x in xrange(w):
                distance = math.hypot(y-self.radius, x-self.radius)
                if distance > self.radius:
                    continue
                powers[y][x] = self.normalizer(self.power, float(distance)/self.radius)

        layer.apply_powers(self.x-self.radius, self.y-self.radius, powers)


class ArrowAreaPoint(BasePowerPoint):

    class Arrow(collections.namedtuple('ArrowBase', ['angle', 'length', 'width'])):
        __slots__ = ()

        @property
        def max_dimension(self): return max(self.length, self.width)

        @property
        def rounded_arrow(self): return self.__class__(angle=math.pi+self.angle,
                                                       length=self.length / 10.0,
                                                       width=self.width)

    def __init__(self, arrows, length_normalizer, width_normalizer, **kwargs):
        super(ArrowAreaPoint, self).__init__(**kwargs)
        self.arrows = arrows
        self.length_normalizer = length_normalizer
        self.width_normalizer = width_normalizer

    def update_powers(self, layer, world):

        radius = max(arrow.length + arrow.width for arrow in self.arrows)

        w = h = 1+radius*2

        if self._powers is None:
            self._powers = self._get_powers_rect(w=w, h=h)
        else:
            layer.apply_powers(self.x-radius, self.y-radius, self._powers)
            return

        powers = self._powers

        for arrow in self.arrows:
            arrow_sin = math.sin(arrow.angle)
            arrow_cos = math.cos(arrow.angle)

            for y in xrange(h):
                for x in xrange(w):
                    point_x = x - radius
                    point_y = y - radius
                    point_distance = math.hypot(point_y, point_x)

                    if point_distance > arrow.length + arrow.width: continue

                    # point_angle = math.atan2(y-radius, x-radius) - arrow.angle

                    # scalar_product / vectors_length_product
                    if point_distance == 0:
                        vector_angle = 0
                    else:
                        vector_angle = (point_x*arrow_cos+point_y*arrow_sin) / (point_distance * 1)
                        vector_angle = math.acos(vector_angle)

                    vector_angle = math.fabs(vector_angle)

                    if vector_angle >= math.pi / 2: continue

                    point_length = point_distance * math.cos(vector_angle)

                    if point_length > arrow.length: continue

                    point_width = point_distance * math.sin(vector_angle)

                    if point_width > arrow.width: continue

                    length_power = self.length_normalizer(self.power, point_length/arrow.length)
                    power = self.width_normalizer(length_power, point_width/arrow.width)
                    powers[y][x] = max(powers[y][x], power)

        layer.apply_powers(self.x-radius, self.y-radius, powers)
