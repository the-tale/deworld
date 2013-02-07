# coding: utf-8

from deworld.layers.base_layer import BaseLayer
from deworld.layers.height_layer import HeightLayer
from deworld.layers.temperature_layer import TemperatureLayer
from deworld.layers.wind_layer import WindLayer
from deworld.layers.wetness_layer import WetnessLayer
from deworld.layers.vegetation_layer import VegetationLayer, VEGETATION_TYPE
from deworld.layers.atmosphere_layer import AtmosphereLayer
from deworld.layers.soil_layer import SoilLayer


class LAYER_TYPE:
    HEIGHT = 0
    TEMPERATURE = 1
    WIND = 2
    WETNESS = 3
    VEGETATION = 4
    ATMOSPHERE = 5
    SOIL = 6

__all__ = [LAYER_TYPE, BaseLayer, HeightLayer, TemperatureLayer, WindLayer, WetnessLayer, AtmosphereLayer, VegetationLayer, SoilLayer, VEGETATION_TYPE]
