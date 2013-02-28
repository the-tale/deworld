# coding: utf-8


class BaseConfig:

    class LAYERS:

        class ATMOSPHERE:
            MAX_WIND_SPEED = 3 # in cells
            DELTA = 3

            WIND_AK = 0.90
            WIND_WK = 1 - WIND_AK

            WIND_FOREST_MULTIPLIER = 0.90

            TEMP_AK = 0.75
            TEMP_WK = 1 - TEMP_AK

            WET_AK = 0.75
            WET_WK = 1 - WET_AK

        class HEIGHT:
            STEP = 0.01

        class TEMPERATURE:
            HEIGHT_PENALTY = 0.5

            POWER_AK = 0.25
            POWER_WK = 1 - POWER_AK

        class VEGETATION:
            HEIGHT_FOREST_BARIER_START = 0.4
            HEIGHT_FOREST_BARIER_END = 0.7
            HEIGHT_GRASS_BARIER_START = 0.6
            HEIGHT_GRASS_BARIER_END = 0.8

            TEMPERATURE_FOREST_BARIER_START = 0.85
            TEMPERATURE_FOREST_BARIER_END = 0.95
            TEMPERATURE_GRASS_BARIER_START = 0.9
            TEMPERATURE_GRASS_BARIER_END = 1.0

            WETNESS_FOREST_BARIER_START = 0.2
            WETNESS_FOREST_BARIER_END = 0.05
            WETNESS_GRASS_BARIER_START = 0.15
            WETNESS_GRASS_BARIER_END = 0.025

            FOREST_BORDER = 0.15
            GRASS_BORDER = 0.05

            SPAWN_PROBABILITY = 0.01

            CURRENT_GRASS_POWER_BONUS = 0.005
            CURRENT_FOREST_POWER_BONUS = 0.03

        class WETNESS:
            STEP = 0.01
            POWER_PER_HEIGHT = -0.25
            POWER_PER_TEMPERATURE = -0.15
            POWER_PER_ATMOSPHERE = 0.5

        class WIND:
            BORDER_SPEED = 0.05
            DELTA = 3
            TEMPERATURE_SPEED = 5.0 /13.0 # PER 100% difference
            HEIGHT_SPEED = 2.5 /13.0 # PER 100% difference

        class SOIL:

            STEP = 0.01

            OPTIMAL_TEMPERATURE = 0.5
            OPTIMAL_WETNESS = 0.5
            OPTIMAL_WIND = 0.5

            # power per 1 delta
            POWER_PER_TEMPERATURE = -0.4
            POWER_PER_WETNESS = -0.4
            POWER_PER_WIND = -0.2

            POWER_PER_VEGETATION_DESERT = -0.2
            POWER_PER_VEGETATION_GRASS = 0.5
            POWER_PER_VEGETATION_FOREST = 0.75
