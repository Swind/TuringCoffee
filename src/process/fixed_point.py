import re
import math
from process import Process
from process import Point


class FixedPoint(Process):
    """
    Example:

        ''' fixed_point
            Coordinates: (0, 0)
            High: 80 mm to 90 mm
            Total Water: 40 ml

            Extrudate: 0.1 ml/step
            Feedrate: 80 mm/min
        '''
    """

    params_rules = {
        # Key:      [Unit,       Required,      Default Value]
        "Coordinates": ["x_y_coordinates", True, None],
        "Total Water": ["capacity",        True, None],
        "High":        ["length_from_to",  True, None],
        "Feedrate":    ["feedrate",        False, 80],
        "Extrudate":   ["extrudate",       True, None]
    }
    def points(self):
        point_number = self.total_water / self.extrudate
        points = map(lambda index: Point(), range(0, int(point_number)))

        points = self.__point_x_y(points)
        points = self.__point_z(points)

        return points

    def __point_x_y(self, points):

        for point in points:
            point.x = self.coordinates[0]
            point.y = self.coordinates[1]

        return points

    def __point_z(self, points):
        z_start = self.high[0]
        z_end = self.high[1]

        z_per_point = (z_end - z_start) / len(points)

        for index, point in enumerate(points):
            point.z = z_start + (z_per_point * index)

        return points
