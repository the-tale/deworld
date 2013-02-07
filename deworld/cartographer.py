# coding: utf-8
import os

try:
    from PIL import Image
except:
    pass

from deworld.map_colors import HeightColorMap, RGBColorMap
from deworld.layers import VEGETATION_TYPE


def draw_image(turn, catalog, layer, power_points, colorizer):

    if not os.path.exists(catalog):
        os.makedirs(catalog)

    img = Image.new('RGB', (layer.w, layer.h))

    data = []
    for row in layer.data:
        for cell in row:
            data.append(colorizer(cell, discret=False).rgb)

    for point in power_points.values():
        data[point.y * layer.w + point.x] = (0, 0, 0)

    img.putdata(data)
    img.save('%s/%.3d.png' % (catalog, turn))

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

def soil_colorizer(soil, discret=False):
    return RGBColorMap.get_color(r=0.0, g=soil, b=0.0)

def atmo_wind_colorizer(point, discret=False):
    return wind_colorizer(point.wind, discret=discret)

def atmo_temperature_colorizer(point, discret=False):
    return temperature_colorizer(point.temperature, discret=discret)

def atmo_wetness_colorizer(point, discret=False):
    return wetness_colorizer(point.wetness, discret=discret)


def draw_world(turn, world, catalog):

    draw_image(turn=turn,
               catalog='%s/%s' % (catalog, 'height'),
               layer=world.layer_height,
               power_points=world.power_points,
               colorizer=HeightColorMap.get_color)

    draw_image(turn=turn,
               catalog='%s/%s' % (catalog, 'temperature'),
               layer=world.layer_temperature,
               power_points=world.power_points,
               colorizer=temperature_colorizer)

    draw_image(turn=turn,
               catalog='%s/%s' % (catalog, 'wind'),
               layer=world.layer_wind,
               power_points=world.power_points,
               colorizer=wind_colorizer)

    draw_image(turn=turn,
               catalog='%s/%s' % (catalog, 'wetness'),
               layer=world.layer_wetness,
               power_points=world.power_points,
               colorizer=wetness_colorizer)

    draw_image(turn=turn,
               catalog='%s/%s' % (catalog, 'vegetation'),
               layer=world.layer_vegetation,
               power_points=world.power_points,
               colorizer=vegetation_colorizer)

    draw_image(turn=turn,
               catalog='%s/%s' % (catalog, 'soil'),
               layer=world.layer_soil,
               power_points=world.power_points,
               colorizer=soil_colorizer)

    draw_image(turn=turn,
               catalog='%s/%s' % (catalog, 'atmo_wind'),
               layer=world.layer_atmosphere,
               power_points=world.power_points,
               colorizer=atmo_wind_colorizer)

    draw_image(turn=turn,
               catalog='%s/%s' % (catalog, 'atmo_temperature'),
               layer=world.layer_atmosphere,
               power_points=world.power_points,
               colorizer=atmo_temperature_colorizer)

    draw_image(turn=turn,
               catalog='%s/%s' % (catalog, 'atmo_wetness'),
               layer=world.layer_atmosphere,
               power_points=world.power_points,
               colorizer=atmo_wetness_colorizer)
