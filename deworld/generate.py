# coding: utf-8
# import os
# import shutil
import math

from PIL import Image

from deworld.world import World
from deworld.layers import LAYER_TYPE
from deworld import power_points
from deworld.map_colors import HeightColorMap, RGBColorMap

# shutil.rmtree('./results', ignore_errors=True)

# os.mkdir('./results')
# os.mkdir('./results/height')
# os.mkdir('./results/temperature')
# os.mkdir('./results/wind')


WIDTH = 100
HEIGHT = 100

world = World(WIDTH, HEIGHT)

linear_normalizer = lambda power, normalized_distance: power*(1-normalized_distance)
equal_normalizer = lambda power, normalized_distance: power

world.add_power_point(power_points.CircleAreaPoint(layer_type=LAYER_TYPE.HEIGHT,
                                                   name='circular_point_1',
                                                   x=25,
                                                   y=25,
                                                   power=0.75,
                                                   radius=15,
                                                   normalizer=linear_normalizer))

world.add_power_point(power_points.CircleAreaPoint(layer_type=LAYER_TYPE.HEIGHT,
                                                   name='circular_point_2',
                                                   x=35,
                                                   y=45,
                                                   power=-0.75,
                                                   radius=15,
                                                   normalizer=linear_normalizer))

arrow_1 = power_points.ArrowAreaPoint.Arrow(angle=-math.pi*5/8, length=60, width=10)
arrow_2 = power_points.ArrowAreaPoint.Arrow(angle=math.pi*5/8, length=30, width=20)

world.add_power_point(power_points.ArrowAreaPoint(layer_type=LAYER_TYPE.HEIGHT,
                                                  name='arrow_point_1',
                                                  x=50,
                                                  y=80,
                                                  power=1.0,
                                                  length_normalizer=linear_normalizer,
                                                  width_normalizer=linear_normalizer,
                                                  arrows=[arrow_1, arrow_1.rounded_arrow,
                                                          arrow_2, arrow_2.rounded_arrow]))

world.add_power_point(power_points.CircleAreaPoint(layer_type=LAYER_TYPE.TEMPERATURE,
                                                   name='temperature_circle',
                                                   x=WIDTH/2,
                                                   y=HEIGHT/2,
                                                   power=0.5,
                                                   radius=int(math.hypot(WIDTH, HEIGHT)/2)+1,
                                                   normalizer=equal_normalizer))


def draw_image(catalog, layer, power_points, colorizer):
    img = Image.new('RGB', (WIDTH, HEIGHT))

    data = []
    for row in layer.data:
        for cell in row:
            data.append(colorizer(cell, discret=False).rgb)

    for point in power_points.values():
        data[point.y * WIDTH + point.x] = (0, 0, 0)

    img.putdata(data)
    img.save('./results/%s/%.3d.png' % (catalog, i))

def wind_colorizer(wind, discret=False):
    r, g, b = 0.5, 0.5, 0.5

    g += wind[0] * 0.5
    b += wind[1] * 0.5

    return RGBColorMap.get_color(r=r, g=g, b=b)

def temperature_colorizer(temp, discret=False):
    r, g, b = 0.5, 0.5, 0.5

    if temp < 0.5:
        b += temp
    else:
        r += (temp - 0.5)

    return RGBColorMap.get_color(r=r, g=g, b=b)


for i in xrange(100):
    print 'do step %d' % i
    world.do_step()

    draw_image(catalog='height',
               layer=world.layer_height,
               power_points=world.power_points,
               colorizer=HeightColorMap.get_color)

    draw_image(catalog='temperature',
               layer=world.layer_temperature,
               power_points=world.power_points,
               colorizer=temperature_colorizer)

    draw_image(catalog='wind',
               layer=world.layer_wind,
               power_points=world.power_points,
               colorizer=wind_colorizer)
