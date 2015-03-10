from __future__ import unicode_literals

from pypeg2 import *
import re

import itertools
import math

from config import *


class Spiral(Namespace):
    """
    Spiral: 1 cm -> 2 cm
        AvgWater: 0.01 ml
        Space: 0.1 mm
        Cylinder: 5
    """
    name = "spiral"
    configs = [Space, AvgWater, Cylinder]

    grammar = "Spiral", ":", attr("start", LengthItem), "->", attr("end", LengthItem), endl, indent(maybe_some(configs))

    def gcode(self):
        start = self.start_point()
        end = self.end_point()

        avg_water = self["avgwater"].get_ml()
        cylinder = self["cylinder"].value
        space = self.__convert_to_mm(float(self["space"].value), self["space"].unit)

        points = self.__points(start, end, space, cylinder, avg_water)

        lines = []
        for point in points:
            template = "G1 X%.4f Y%.4f E%.4f"
            tmp = template % point

            lines.append(tmp)

        return lines

    def info(self):
        pass

    def __points(self, start, end, space, cylinder, avg_water):
        theta = 10

        cylinder = int(cylinder)

        a = float(end - start) / int(cylinder) / 360
        radius = start

        total_theta = 0
        max_theta = cylinder * 360

        point_list = []

        while (total_theta <= max_theta):
            # space / (2 * pi * r) * 360 = theta
            now_radius = a * total_theta + radius

            now_theta = (space / ( 2 * math.pi * now_radius)) * 360
            total_theta = total_theta + now_theta

            x, y = self.__point(now_radius, total_theta)

            point_list.append((x, y, avg_water))

        return point_list

    def __point(self, radius, theta):
        x = radius * math.cos(theta * math.pi / 180)
        y = radius * math.sin(theta * math.pi / 180)

        return (x, y)

    def __convert_to_mm(self, value, unit):
        if unit == "cm":
            return value * 10
        else:
            return value

    def start_point(self):
        return self.__convert_to_mm(float(self.start.value), self.start.unit)

    def end_point(self):
        return self.__convert_to_mm(float(self.end.value), self.end.unit)
