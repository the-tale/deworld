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

        powers = self._powers

        for y in range(h):

            if self.y + y - self.radius < 0 or self.y + y - self.radius >= world.h: continue

            for x in range(w):

                if self.x + x - self.radius < 0 or self.x + x - self.radius >= world.w: continue

                distance = math.hypot(y-self.radius, x-self.radius)
                if distance > self.radius:
                    continue
                powers[y][x] = self.normalizer(self.power(world, self.x+x-self.radius, self.y+y-self.radius), float(distance)/self.radius)

        layer.apply_powers(self.x-self.radius, self.y-self.radius, powers)
