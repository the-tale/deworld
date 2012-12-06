# coding: utf-8

import math

from deworld.layers.base_layer import BaseLayer


class WindLayer(BaseLayer):

    BORDER_SPEED = 0.0 #10.0
    # DISTANCE_SPEED = 1.5 # PEAR 1 DISTANCE
    TEMPERATURE_SPEED = 5.0 # PER 1 DEGREE
    HEIGHT_SPEED = 3.0 # PER 1 HEIGHT DELTA

    def __init__(self, **kwargs):
        super(WindLayer, self).__init__(default=(0.0, 0.0), **kwargs)

    def get_normalized_data(self): return self.data

    def _modify_speed(self,
                      speed, # current wind speed
                      temp_delta, # temp delta between from and to
                      height_delta, # height delta between from and to
                      distance, # distance between from and tob
                      direction # direction from "from" to "to"
                      ):
        # speed_sign = math.copysign(1.0, speed)

        # distance always decrease speed

        # speed = sign * distance * self.DISTANCE_SPEED

        # speed increased from lower temperature to highest
        speed += direction * temp_delta * self.TEMPERATURE_SPEED

        # mountains only decrease speed
        # if height_delta < 0 and (speed_sign * sign > 0):
        speed += math.fabs(height_delta) * self.HEIGHT_SPEED

        return speed
        # if speed < -self.MAX: speed = -self.MAX
        # if speed > self.MAX: speed = self.MAX

    def _get_speeds(self, from_x, from_y, to_x, to_y):
        if not (0 <= from_x < self.w and 0 <= from_y < self.h):
            v_speed, h_speed = 0.0, 0.0
            if from_x < 0:
                v_speed = self.BORDER_SPEED
            elif from_x >= self.w:
                v_speed = -self.BORDER_SPEED

            if from_y < 0:
                h_speed = self.BORDER_SPEED
            elif from_y >= self.h:
                h_speed = -self.BORDER_SPEED

            return v_speed, h_speed

        v_speed, h_speed = 0, 0 #self.data[from_y][from_x] #self._get_base_wind(from_x, from_y)

        from_temp = self.world.layer_temperature.data[from_y][to_x]
        to_temp = self.world.layer_temperature.data[to_y][to_x]

        from_height = self.world.layer_height.data[from_y][to_x]
        to_height = self.world.layer_height.data[to_y][to_x]

        if from_x != to_x and from_y != to_y:
            distance = 1.44
        elif from_x != to_x or from_y != to_y:
            distance = 1.0
        else:
            distance = 0.0

        v_speed = self._modify_speed(speed=v_speed,
                                     temp_delta=from_temp-to_temp, # if from_x != to_x else 0.0,
                                     height_delta=from_height-to_height, # if from_x != to_x else 0.0,
                                     distance=distance,
                                     direction=math.copysign(1.0, to_x - from_x))

        h_speed = self._modify_speed(speed=h_speed,
                                     temp_delta=from_temp-to_temp, # if from_y != to_y else 0.0,
                                     height_delta=from_height-to_height, # if from_y != to_y else 0.0,
                                     distance=distance,
                                     direction=math.copysign(1.0, to_y - from_y))

        return ( v_speed, h_speed)


    def _calculate_wind(self, x, y):
        winds = (self._get_speeds(x-1, y-1, x, y),
                 self._get_speeds(x  , y-1, x, y),
                 self._get_speeds(x+1, y-1, x, y),
                 self._get_speeds(x-1, y  , x, y),
                 # self._get_speeds(x  , y  , x, y),
                 self._get_speeds(x+1, y  , x, y),
                 self._get_speeds(x-1, y+1, x, y),
                 self._get_speeds(x  , y+1, x, y),
                 self._get_speeds(x+1, y+1, x, y)
            )

        v_speeds, h_speeds = zip(*winds)
        v_speed = sum(v_speeds)
        h_speed = sum(h_speeds)

        if v_speed < -self.MAX: v_speed = -self.MAX
        if v_speed > self.MAX: v_speed = self.MAX
        if h_speed < -self.MAX: h_speed = -self.MAX
        if h_speed > self.MAX: h_speed = self.MAX

        return v_speed, h_speed


    def sync(self):

        for y in xrange(0, self.h):
            for x in xrange(0, self.w):
                self.next_data[y][x] = self._calculate_wind(x, y)
