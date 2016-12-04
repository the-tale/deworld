# coding: utf-8

import math
import collections

from deworld.power_points.base_point import BasePoint

class ArrowAreaPoint(BasePoint):

    class Arrow(collections.namedtuple('ArrowBase', ['angle', 'length', 'width'])):
        __slots__ = ()

        @property
        def max_dimension(self): return max(self.length, self.width)

        @property
        def rounded_arrow(self): return self.__class__(angle=math.pi+self.angle,
                                                       length=self.length / 5.0,
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

        powers = self._powers

        for arrow in self.arrows:
            arrow_sin = math.sin(arrow.angle)
            arrow_cos = math.cos(arrow.angle)

            for y in range(h):

                if self.y + y - radius < 0 or self.y + y - radius >= world.h: continue

                for x in range(w):

                    if self.x + x - radius < 0 or self.x + x - radius >= world.w: continue

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
                        vector_angle = math.acos(round(vector_angle, 8))

                    vector_angle = math.fabs(vector_angle)

                    if vector_angle >= math.pi / 2: continue

                    point_length = point_distance * math.cos(vector_angle)

                    if point_length > arrow.length: continue

                    point_width = point_distance * math.sin(vector_angle)

                    if point_width > arrow.width: continue

                    length_power = self.length_normalizer(self.power(world, self.x+x-radius, self.y+y-radius), point_length/arrow.length)
                    power = self.width_normalizer(length_power, point_width/arrow.width)
                    powers[y][x] = max(powers[y][x], power)

        layer.apply_powers(self.x-radius, self.y-radius, powers)
