# coding: utf-8
# import numpy
import math

class WorldException(Exception): pass

class LAYER_TYPE:
    HEIGHT = 0
    TEMPERATURE = 1

def copy2d(original):
    data = [None] * len(original)
    for i, row in enumerate(original):
        data[i] = row[:]
    return data

class BaseLayer(object):

    MAX = 100

    def __init__(self, world, w, h, default=0.0):
        self.world = world
        self.w = w
        self.h = h

        # self.base_data = numpy.empty(shape=(self.h, self.w), dtype=default.__class__)
        # self.base_data.fill(default)
        # self.data = self.base_data.copy()
        # self.power = self.base_data.copy()
        # self.next_data = self.base_data.copy()
        self.base_data = []
        for y in xrange(0, h):
            self.base_data.append([default] * w)
        self.data = copy2d(self.base_data)
        self.power = copy2d(self.base_data)
        self.next_data = copy2d(self.base_data)

    def get_normalized_data(self):
        data = copy2d(self.base_data)
        for y in xrange(self.h):
            for x in xrange(self.w):
                data[y][x] = self.data[y][x] / float(self.MAX)
        return data
        # return self.data / float(self.MAX)

    def add_power(self, x, y, power):
        self.power[y][x] += power

    def apply_powers(self, x, y, powers):

        for i, row in enumerate(powers):
            if y+i < 0 or self.h <= y+i : continue

            for j, power in enumerate(row):
                if x+j < 0 or self.w <= x+j : continue

                self.add_power(x+j, y+i, power)

    def sync(self):
        # power on base of last step data and current power
        pass

    def apply(self):
        # self.data[:] = self.next_data
        self.data = copy2d(self.next_data)

class HeightLayer(BaseLayer):

    def __init__(self, **kwargs):
        super(HeightLayer, self).__init__(default=self.MAX/2, **kwargs)


    def sync(self):

        for y in xrange(0, self.h):
            for x in xrange(0, self.w):
                original_value = self.data[y][x]
                power_points = self.power[y][x]

                if power_points > original_value:
                    self.next_data[y][x] = min(original_value + 1, self.MAX)
                elif power_points < original_value - self.MAX / 2:
                    self.next_data[y][x] = max(original_value - 1, 0)

                self.power[y][x] = 0


class TemperatureLayer(BaseLayer):

    HEIGHT_MULTIPLYER = 0.5

    def __init__(self, **kwargs):
        super(TemperatureLayer, self).__init__(default=0, **kwargs)

    def sync(self):

        for y in xrange(0, self.h):
            for x in xrange(0, self.w):
                original_value = self.data[y][x]
                power_points = self.power[y][x]

                # modify power on base of height
                height_norm = (float(self.world.layer_height.data[y][x]) /
                               self.world.layer_height.MAX)
                power_points *= self.HEIGHT_MULTIPLYER * height_norm

                if power_points > original_value:
                    self.next_data[y][x] = min(original_value + 1, self.MAX)
                elif power_points < original_value:
                    self.next_data[y][x] = max(original_value - 1, 0)

                self.power[y][x] = -self.next_data[y][x] # we lost temperature every step


class WindLayer(BaseLayer):

    BORDER_SPEED = 0.0 #10.0
    DISTANCE_SPEED = 1.5 # PEAR 1 DISTANCE
    TEMPERATURE_SPEED = 2.0 # PER 1 DEGREE
    HEIGHT_SPEED = 1.0 # PER 1 HEIGHT DELTA

    def __init__(self, **kwargs):
        super(WindLayer, self).__init__(default=(0.0, 0.0), **kwargs)

    def get_normalized_data(self): return self.data

    def _modify_speed(self,
                      speed, # current wind speed
                      temp_delta, # temp delta between from and to
                      height_delta, # height delta between from and to
                      distance, # distance between from and tob
                      sign # direction from "from" to "to"
                      ):
        speed_sign = math.copysign(1.0, speed)

        # distance always decrease speed
        speed -= speed_sign * distance * self.DISTANCE_SPEED

        # speed increased from lower temperature to highest
        speed += sign * temp_delta * self.TEMPERATURE_SPEED

        # mountains only decrease speed
        if height_delta < 0 and (speed_sign * sign > 0):
            speed -= speed_sign * (math.fabs(height_delta)) * self.HEIGHT_SPEED

        if speed_sign * speed < 0:
            return 0

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

        v_speed, h_speed = self.data[from_y][from_x] #self._get_base_wind(from_x, from_y)

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
                                     temp_delta=from_temp-to_temp if from_x != to_x else 0.0,
                                     height_delta=from_height-to_height if from_x != to_x else 0.0,
                                     distance=distance,
                                     sign=math.copysign(1.0, from_x - to_x))

        h_speed = self._modify_speed(speed=h_speed,
                                     temp_delta=from_temp-to_temp if from_y != to_y else 0.0,
                                     height_delta=from_height-to_height if from_y != to_y else 0.0,
                                     distance=distance,
                                     sign=math.copysign(1.0, from_y - to_y))

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



class World(object):

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.power_points = {}

        self.layer_height = HeightLayer(world=self, w=self.w, h=self.h)
        self.layer_temperature = TemperatureLayer(world=self, w=self.w, h=self.h)
        self.layer_wind = WindLayer(world=self, w=self.w, h=self.h)

    def add_power_point(self, power_point):
        if power_point.name in self.power_points:
            raise WorldException('try to add duplicate power point "%s"' % power_point.name)
        self.power_points[power_point.name] = power_point


    def do_step(self):

        for power_point in self.power_points.values():
            power_point.update_world(self)

        self.layer_height.sync()
        self.layer_temperature.sync()
        self.layer_wind.sync()

        self.layer_height.apply()
        self.layer_temperature.apply()
        self.layer_wind.apply()
