import re
import math
from process import Process
from process import Point


class Circle(Process):
    """
    Example:

    ''' circle

        Radius: 1 cm
        High: 80 -> 90
        Total Water: 40 ml
        Feedrate: 80 mm/min
        Extrudate: 1 ml/mm
        Point interval: 0.01 mm
    '''
    """

    params_rules = {
        # Key:      [Unit,       Required,      Default Value]
        "Water":          ["capacity", True],
        "Velocity":       ["velocity", True],
        "Radius":         ["length",   True],
        "Extrudate":      ["extrudate", True],
        "Feedrate":       ["feedrate", False, 80],
        "Point interval": ["length",   False, 0.01]
    }

    def points(self, previous_end_point=None):
        if previous_end_point:
            start_angle = math.atan2(previous_end_point.y, previous_end_point.x)
        else:
            start_angle = 0

        total_length = self.__water / self.__extrudate
        point_number = total_length / self.__point_interval

        # Init all points
        points = [Point(None, None, None, None, None)] * point_number

        points = self.__point_xy(points, start_angle)
        points = self.__point_e(points)
        points = self.__point_z(points)

        return points

    def __point_xy(self, points, start_angle):
        circumference = 2 * math.pi * self.__radius
        total_length = self.__water / self.__extrudate
        point_number = len(points)

        cylinder = total_length / circumference

        av = (2 * math.pi * cylinder) / point_number

        for index, point in enumerate(points):
            point.x = self.__radius * math.cos(av * index + start_angle)
            point.y = self.__radius * math.sin(av * index + start_angle)

        return points

    def __point_e(self, points):
        extrudate_per_point = self.__extrudate * self._point_interval

        for point in points:
            point.e1 = extrudate_per_point

        return points

    def __point_z(self, points):
        z_start = self.__high[0]
        z_end = self.__high[1]

        z_per_point = (z_end - z_start) / len(points)

        for index, point in enumerate(points):
            point.z = z_start + (z_per_point * index)

        return points

if __name__ == "__main__":
    pass
