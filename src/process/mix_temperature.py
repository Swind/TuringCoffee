from process import Process
from process import Point


class MixTemperature(Process):

    """
    Example:

        ''' mix temperature
            Total Water: 40 ml
            Temperature: 65 degress C
        '''
    """

    params_rules = {
        # Key:      [Unit,       Required,      Default Value]
        'Total Water': ['capacity',        True, None],
        'Temperature':    ['temperature', False, None],
    }

    def points(self):
        point_number = self.total_water * 10
        points = map(lambda index: Point(), range(0, int(point_number)))

        points = self.__point_e1(points)
        points = self.__point_f(points)
        points.insert(0, Point(x=-80, y=50, z=260, f=2000))

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
        e1 = self.total_water / len(points)

        for point in points:
            point.e1 = e1

        return points

    def __point_f(self, points):
        f = 100
        for point in points:
            point.f = f
        return points
