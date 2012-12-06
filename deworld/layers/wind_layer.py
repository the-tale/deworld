# coding: utf-8

import math

from deworld.layers.base_layer import BaseLayer

from deworld.utils import E


class WindLayer(BaseLayer):

    BORDER_SPEED = 10.0
    DELTA = 3
    TEMPERATURE_SPEED = 1.0 # PER 1 DEGREE
    HEIGHT_SPEED = 0.5 # PER 1 HEIGHT DELTA

    def __init__(self, **kwargs):
        super(WindLayer, self).__init__(default=(0.0, 0.0), **kwargs)

    def get_normalized_data(self): return self.data

    def _break_speed(self, angle, speed):
        return math.cos(angle)*speed,  math.sin(angle)*speed

    def _get_speeds(self, from_x, from_y, to_x, to_y):
        angle = math.atan2(to_y-from_y, to_x-from_x)

        if not (0 <= from_x < self.w and 0 <= from_y < self.h):
            return self._break_speed(angle, self.BORDER_SPEED)

        from_temp = self.world.layer_temperature.data[from_y][from_x]
        to_temp = self.world.layer_temperature.data[to_y][to_x]
        temp_multiplier = self.TEMPERATURE_SPEED * (from_temp - to_temp)
        temp_speed = self._break_speed(angle, temp_multiplier)

        from_height = self.world.layer_height.data[from_y][from_x]
        to_height = self.world.layer_height.data[to_y][to_x]
        height_multiplier = self.HEIGHT_SPEED * (from_height - to_height)
        height_speed = self._break_speed(angle, height_multiplier)

        distance = 1
        if from_x != to_x or from_y != to_y:
            distance = math.hypot(from_x-to_x, from_y-to_y)

        v_speed = (temp_speed[0] + height_speed[0]) / distance
        h_speed = (temp_speed[1] + height_speed[1]) / distance

        return ( v_speed, h_speed)


    def _calculate_wind(self, x, y):
        winds = []
        for _y in xrange(y-self.DELTA, y+self.DELTA+1):
            for _x in xrange(x-self.DELTA, x+self.DELTA+1):
                winds.append(self._get_speeds(_x, _y, x, y))

        v_speeds, h_speeds = zip(*winds)
        v_speed = sum(v_speeds)
        h_speed = sum(h_speeds)

        if v_speed < -self.MAX: v_speed = -self.MAX
        if v_speed > self.MAX: v_speed = self.MAX
        if h_speed < -self.MAX: h_speed = -self.MAX
        if h_speed > self.MAX: h_speed = self.MAX

        return v_speed, h_speed

    def _smooth_wind(self, x, y):

        v_speed, h_speed = self.next_data[y][x]

        if not (-E < v_speed < E and -E < h_speed < E):
            return v_speed, h_speed

        winds = []
        for _y in xrange(y-self.DELTA, y+self.DELTA+1):
            for _x in xrange(x-self.DELTA, x+self.DELTA+1):
                if not (0 <= _x < self.w and 0 <= _y < self.h):
                    angle = math.atan2(y-_y, x-_x)
                    speed = self._break_speed(angle, self.BORDER_SPEED)
                else:
                    speed = self.data[_y][_x]

                v_speed, h_speed = speed
                if -E < v_speed < E and -E < h_speed < E:
                    continue

                winds.append(speed)

        if not winds:
            return 0.0, 0.0

        v_speeds, h_speeds = zip(*winds)
        v_speed = sum(v_speeds) / len(winds)
        h_speed = sum(h_speeds) / len(winds)

        return v_speed, h_speed


    def sync(self):

        for y in xrange(0, self.h):
            for x in xrange(0, self.w):
                self.next_data[y][x] = self._calculate_wind(x, y)

        for y in xrange(0, self.h):
            for x in xrange(0, self.w):
                self.next_data[y][x] = self._smooth_wind(x, y)
