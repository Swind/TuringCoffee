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
        'Coordinates': ['x_y_coordinates', True, None],
        'Total Water': ['capacity',        True, None],
        'High':        ['length_from_to',  True, None],
        'Feedrate':    ['feedrate',        False, 80],
        'Extrudate':   ['extrudate',       True, None]
    }

    def points(self):
        point_number = self.total_water / self.extrudate
        points = map(lambda index: Point(), range(0, int(point_number)))

        #points = self.__point_x_y(points)
        #points = self.__point_z(points)
        points = self.__point_e1(points)
        points = self.__point_f(points)

        x = self.coordinates[0]
        y = self.coordinates[1]
        points.insert(0, Point(x=x, y=y, f=2000))
        if self.high[0] != self.high[1]:
            points = self.__point_z(points)
        else:
            z = self.high[0]
            points.insert(0, Point(z=z, f=2000))

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

    def __point_e1(self, points):
        e1 = self.extrudate

        for point in points:
            point.e1 = e1

        return points

    def __point_f(self, points):
        f = self.feedrate
        for point in points:
            point.f = f
        return points
