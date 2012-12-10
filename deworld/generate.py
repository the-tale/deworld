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

world.add_power_point(power_points.CircleAreaPoint(layer_type=LAYER_TYPE.HEIGHT,
                                                   name='circular_point_1',
                                                   x=25,
                                                   y=25,
                                                   power=0.75,
                                                   radius=15,
                                                   normalizer=normalizers.linear))

world.add_power_point(power_points.CircleAreaPoint(layer_type=LAYER_TYPE.HEIGHT,
                                                   name='circular_point_2',
                                                   x=35,
                                                   y=45,
                                                   power=-0.75,
                                                   radius=15,
                                                   normalizer=normalizers.linear))

arrow_1 = power_points.ArrowAreaPoint.Arrow(angle=-math.pi*5/8, length=60, width=10)
arrow_2 = power_points.ArrowAreaPoint.Arrow(angle=math.pi*5/8, length=30, width=20)

world.add_power_point(power_points.ArrowAreaPoint(layer_type=LAYER_TYPE.HEIGHT,
                                                  name='arrow_point_1',
                                                  x=50,
                                                  y=80,
                                                  power=1.0,
                                                  length_normalizer=normalizers.linear,
                                                  width_normalizer=normalizers.linear,
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

for i in xrange(300):
    print 'do step %d' % i
    world.do_step()
    draw_world(i, world, catalog='./results')
