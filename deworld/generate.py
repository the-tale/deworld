# coding: utf-8
# import os
# import shutil
import math

from deworld.world import World
from deworld.layers import LAYER_TYPE
from deworld import power_points
from deworld.configs import BaseConfig
from deworld import normalizers
from deworld.cartographer import draw_world

# shutil.rmtree('./results', ignore_errors=True)

# os.mkdir('./results')
# os.mkdir('./results/height')
# os.mkdir('./results/temperature')
# os.mkdir('./results/wind')

WIDTH = 100
HEIGHT = 100

world = World(w=WIDTH, h=HEIGHT, config=BaseConfig)

def get_height_power_function(borders, power_percent=1.0):

    def power_function(world, x, y):
        height = world.layer_height.data[y][x]

        if height < borders[0]: return (0.0, math.fabs(borders[0] - height) * power_percent)
        if height > borders[1]: return (math.fabs(borders[1] - height) * power_percent, 0.0)

        optimal = (borders[0] + borders[1]) / 2

        if height < optimal: return (0.0, math.fabs(borders[0] - height) / 2 * power_percent)
        if height > optimal: return (math.fabs(borders[1] - height) / 2 * power_percent, 0.0)

        return (0.0, 0.0)

    return power_function

world.add_power_point(power_points.CircleAreaPoint(layer_type=LAYER_TYPE.HEIGHT,
                                                   name='circular_point_1',
                                                   x=25,
                                                   y=25,
                                                   power=get_height_power_function(borders=(-0.5, 0.5)),
                                                   default_power=(0,0),
                                                   radius=15,
                                                   normalizer=normalizers.linear_2))

world.add_power_point(power_points.CircleAreaPoint(layer_type=LAYER_TYPE.HEIGHT,
                                                   name='circular_point_2',
                                                   x=35,
                                                   y=45,
                                                   power=get_height_power_function(borders=(0.25, 0.75)),
                                                   default_power=(0,0),
                                                   radius=15,
                                                   normalizer=normalizers.linear_2))

arrow_1 = power_points.ArrowAreaPoint.Arrow(angle=-math.pi*5/8, length=60, width=10)
arrow_2 = power_points.ArrowAreaPoint.Arrow(angle=math.pi*5/8, length=30, width=20)

world.add_power_point(power_points.ArrowAreaPoint(layer_type=LAYER_TYPE.HEIGHT,
                                                  name='arrow_point_1',
                                                  x=50,
                                                  y=80,
                                                  power=lambda w,x,y: (1.0, 0),
                                                  default_power=(0,0),
                                                  length_normalizer=normalizers.linear_2,
                                                  width_normalizer=normalizers.linear_2,
                                                  arrows=[arrow_1, arrow_1.rounded_arrow,
                                                          arrow_2, arrow_2.rounded_arrow]))

world.add_power_point(power_points.CircleAreaPoint(layer_type=LAYER_TYPE.TEMPERATURE,
                                                   name='temperature_circle',
                                                   x=WIDTH/2,
                                                   y=HEIGHT/2,
                                                   power=0.5,
                                                   radius=int(math.hypot(WIDTH, HEIGHT)/2)+1,
                                                   normalizer=normalizers.equal))


world.add_power_point(power_points.CircleAreaPoint(layer_type=LAYER_TYPE.WETNESS,
                                                   name='wetness_circle',
                                                   x=WIDTH/2,
                                                   y=HEIGHT/2,
                                                   power=0.5,
                                                   radius=int(math.hypot(WIDTH, HEIGHT)/2)+1,
                                                   normalizer=normalizers.equal))

# vegetation
world.add_power_point(power_points.CircleAreaPoint(layer_type=LAYER_TYPE.VEGETATION,
                                                   name='vegetation_circle',
                                                   x=WIDTH/2,
                                                   y=HEIGHT/2,
                                                   power=(0.3, 0.3),
                                                   radius=int(math.hypot(WIDTH, HEIGHT)/2)+1,
                                                   normalizer=normalizers.equal,
                                                   default_power=(0.0, 0.0)))

world.add_power_point(power_points.CircleAreaPoint(layer_type=LAYER_TYPE.VEGETATION,
                                                   name='vegetation_grass_left',
                                                   x=20,
                                                   y=20,
                                                   power=(0.3, 0.0),
                                                   radius=(WIDTH+HEIGHT)/4,
                                                   normalizer=normalizers.linear_2,
                                                   default_power=(0.0, 0.0)))

world.add_power_point(power_points.CircleAreaPoint(layer_type=LAYER_TYPE.VEGETATION,
                                                   name='vegetation_forest_left',
                                                   x=20,
                                                   y=80,
                                                   power=(0.0, 0.3),
                                                   radius=(WIDTH+HEIGHT)/4,
                                                   normalizer=normalizers.linear_2,
                                                   default_power=(0.0, 0.0)))

for i in range(300):
    print('do step %d' % i)
    world.do_step()
    draw_world(i, world, catalog='./results')
