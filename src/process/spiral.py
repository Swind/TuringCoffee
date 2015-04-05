import re
import math
from process import Process
from process import Point


class Spiral(Process):
    """
    Example:

        ''' spiral
            Radius: 1 cm to 2 cm
            High: 80 mm to 90 mm

            Cylinder: 5

            Point interval: 0.01 mm
            Feedrate: 80 mm/min
            Extrudate: 1 ml/mm
        '''
    """
    params_rules = {
        # Key:      [Unit,       Required,      Default Value]
        "Radius":         ["length_from_to",    True, None],
        "High":           ["length_from_to",      True, None],
        "Cylinder":       [None,  True, None],
        "Point interval": ["length",    False, 0.01],
        "Feedrate":       ["feedrate",  False, 80],
        "Extrudate":      ["extrudate", True, None],
    }

    def points(self):
        max_theta = math.radians(self.cylinder * 360)
        a = (self.radius[1] - self.radius[0]) / max_theta

        total_theta = 0
        point_list = []

        while (total_theta <= max_theta):
            # point interval / (2 * pi * r) = theta
            now_radius = a * total_theta + self.radius[0]
            now_theta = math.radians((self.point_interval / (2*math.pi*now_radius))*360)

            total_theta = total_theta + now_theta

            x = now_radius * math.cos(total_theta)
            y = now_radius * math.sin(total_theta)

            point_list.append(Point(x=x, y=y))

        point_list = self.__point_e(point_list)
        point_list = self.__point_z(point_list)
        point_list = self.__point_f(point_list)

        return point_list

    def __point_e(self, points):
        extrudate_per_point = self.extrudate * self.point_interval

        for point in points:
            point.e1 = extrudate_per_point

        return points

    def __point_z(self, points):
        z_start = self.high[0]
        z_end = self.high[1]

        z_per_point = (z_end - z_start) / len(points)

        for index, point in enumerate(points):
            point.z = z_start + (z_per_point * index)

        # Quick move to the z start point
        quick_move = Point(z=z_start, f=1000)
        points.insert(0, quick_move)

        return points

    def __point_f(self, points):
        f = self.feedrate
	for point in points:
	    point.f = f
        return points
