# coding: utf-8

import math

from deworld.power_points.base_point import BasePoint

class CircleAreaPoint(BasePoint):

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
