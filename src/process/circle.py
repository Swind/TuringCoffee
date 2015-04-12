import math
from process import Process
from process import Point


class Circle(Process):

    """
    Example:

        ''' circle

            Radius: 1 cm
            High: 80 mm to 90 mm
            Total Water: 40 ml
            Feedrate: 80 mm/min
            Extrudate: 0.1 ml/mm
            Point interval: 0.01 mm
        '''
    """

    params_rules = {
        # Key:      [Unit,       Required,      Default Value]
        'Total Water':          ['capacity',  True, None],
        'Radius':         ['length',    True, None],
        'Extrudate':      ['extrudate', True, None],
        'High':           ['length_from_to',      True, None],
        'Feedrate':       ['feedrate',  False, 80],
        'Point interval': ['length',    False, 0.01]
    }

    def points(self, previous_end_point=None):
        if previous_end_point:
            start_angle = math.atan2(
                previous_end_point.y, previous_end_point.x)
        else:
            start_angle = 0

        total_length = self.total_water / self.extrudate
        point_number = total_length / self.point_interval

        # Init all points

        points = map(lambda index: Point(), range(0, int(point_number)))
        points = self.__point_xy(points, start_angle)
        points = self.__point_e(points)
        points = self.__point_z(points)
        points = self.__point_f(points)

        return points

    def total_water(self):
        return self.total_water

    def total_length(self):
        return (self.total_water / self.extrudate) + math.fabs((self.high[1] - self.high[0]))

    def __point_xy(self, points, start_angle):
        circumference = 2 * math.pi * self.radius
        total_length = self.total_water / self.extrudate
        point_number = len(points)

        cylinder = total_length / circumference

        av = (2 * math.pi * cylinder) / point_number

        for index, point in enumerate(points):
            point.x = self.radius * math.cos(av * index + start_angle)
            point.y = self.radius * math.sin(av * index + start_angle)

        return points

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

if __name__ == '__main__':
    pass
