from __future__ import unicode_literals

from pypeg2 import *
import re

import itertools

import matplotlib.pyplot as plt
import numpy as np

from config import *

class Origin(Namespace):
    """
    Origin:
        Water: 20 ml
        AvgWater: 0.01 ml
    """
    name = "origin"
    grammar = "Origin", ":", endl, indent(maybe_some([Water, AvgWater]))

    def gcode(self):
        water = self["water"].get_ml()
        avg_water = self["avgwater"].get_ml()

        lines = []
        for index in range(0, int(water / avg_water)):
            lines.append("G1 X0 Y0 E%.4f" % avg_water)

        return lines
