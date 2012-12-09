# coding: utf-8
# import os
# import shutil
import math

from PIL import Image

from deworld.world import World
from deworld.layers import LAYER_TYPE, VEGETATION_TYPE
from deworld import power_points
from deworld.map_colors import HeightColorMap, RGBColorMap
from deworld.configs import BaseConfig

# shutil.rmtree('./results', ignore_errors=True)

# os.mkdir('./results')
# os.mkdir('./results/height')
# os.mkdir('./results/temperature')
# os.mkdir('./results/wind')

WIDTH = BaseConfig.WIDTH
HEIGHT = BaseConfig.HEIGHT

world = World(config=BaseConfig)

linear_normalizer = lambda power, normalized_distance: power*(1-normalized_distance)
equal_normalizer = lambda power, normalized_distance: power
linear_2_normalizer = lambda power, normalized_distance: (power[0]*(1-normalized_distance), power[1]*(1-normalized_distance))

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


world.add_power_point(power_points.CircleAreaPoint(layer_type=LAYER_TYPE.WETNESS,
                                                   name='wetness_circle',
                                                   x=WIDTH/2,
                                                   y=HEIGHT/2,
                                                   power=0.5,
                                                   radius=int(math.hypot(WIDTH, HEIGHT)/2)+1,
                                                   normalizer=equal_normalizer))

# vegetation
world.add_power_point(power_points.CircleAreaPoint(layer_type=LAYER_TYPE.VEGETATION,
                                                   name='vegetation_circle',
                                                   x=WIDTH/2,
                                                   y=HEIGHT/2,
                                                   power=(0.3, 0.3),
                                                   radius=int(math.hypot(WIDTH, HEIGHT)/2)+1,
                                                   normalizer=equal_normalizer,
                                                   default_power=(0.0, 0.0)))

world.add_power_point(power_points.CircleAreaPoint(layer_type=LAYER_TYPE.VEGETATION,
                                                   name='vegetation_grass_left',
                                                   x=20,
                                                   y=20,
                                                   power=(0.3, 0.0),
                                                   radius=(WIDTH+HEIGHT)/4,
                                                   normalizer=linear_2_normalizer,
                                                   default_power=(0.0, 0.0)))

world.add_power_point(power_points.CircleAreaPoint(layer_type=LAYER_TYPE.VEGETATION,
                                                   name='vegetation_forest_left',
                                                   x=20,
                                                   y=80,
                                                   power=(0.0, 0.3),
                                                   radius=(WIDTH+HEIGHT)/4,
                                                   normalizer=linear_2_normalizer,
                                                   default_power=(0.0, 0.0)))


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

def wetness_colorizer(wetness, discret=False):
    return RGBColorMap.get_color(r=1.0-wetness, g=1.0-wetness, b=1.0)

def vegetation_colorizer(vegetation, discret=False):
    if vegetation == VEGETATION_TYPE.GRASS:
        return RGBColorMap.get_color(r=55.0/256, g=200.0/256, b=55.0/256)
    if vegetation == VEGETATION_TYPE.FOREST:
        return RGBColorMap.get_color(r=55.0/256, g=125.0/256, b=55.0/256)
    if vegetation == VEGETATION_TYPE.DESERT:
        return RGBColorMap.get_color(r=244.0/256, g=164.0/256, b=96.0/256)

    return RGBColorMap.get_color(r=0.0, g=0.0, b=0.0)

def atmo_wind_colorizer(point, discret=False):
    return wind_colorizer(point.wind, discret=discret)

def atmo_temperature_colorizer(point, discret=False):
    return temperature_colorizer(point.temperature, discret=discret)

def atmo_wetness_colorizer(point, discret=False):
    return wetness_colorizer(point.wetness, discret=discret)


for i in xrange(300):
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

    draw_image(catalog='wetness',
               layer=world.layer_wetness,
               power_points=world.power_points,
               colorizer=wetness_colorizer)

    draw_image(catalog='vegetation',
               layer=world.layer_vegetation,
               power_points=world.power_points,
               colorizer=vegetation_colorizer)

    draw_image(catalog='atmo_wind',
               layer=world.layer_atmosphere,
               power_points=world.power_points,
               colorizer=atmo_wind_colorizer)

    draw_image(catalog='atmo_temperature',
               layer=world.layer_atmosphere,
               power_points=world.power_points,
               colorizer=atmo_temperature_colorizer)

    draw_image(catalog='atmo_wetness',
               layer=world.layer_atmosphere,
               power_points=world.power_points,
               colorizer=atmo_wetness_colorizer)
