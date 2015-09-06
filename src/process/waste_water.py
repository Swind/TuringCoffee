from process import Process
from process import Point


class WasteWater(Process):

    """
    Example:

        ''' waste water
            Cold Water: 100 ml
            Hot Water: 150 ml
        '''
    """

    params_rules = {
        'Cold Water': ['capacity', True, None],
        'Hot Water': ['capacity', True, None]
    }

    def points(self):

        cold_point_number = int(self.cold_water)
        cold_points = map(lambda index: Point(), range(0, int(cold_point_number) * 10))
        cold_points = self.__point_e2(cold_points)
        cold_points = self.__point_f2(cold_points)

        hot_point_number = int(self.hot_water)
        hot_points = map(lambda index: Point(), range(0, int(hot_point_number)))
        hot_points = self.__point_e1(hot_points)
        hot_points = self.__point_f(hot_points)

        points = []
        points.extend(cold_points)
        points.extend(hot_points)

        points.insert(0, Point(x=-80, y=50, z=260, f=2000))

        return points

    def __point_x_y(self, points):

        for point in points:
            point.x = -80
            point.y = 50

        return points

    def __point_z(self, points):
        for index, point in enumerate(points):
            point.z = 260
        return points

    def __point_e1(self, points):
        for point in points:
            point.e1 = 1.0
        return points

    def __point_e2(self, points):
        for point in points:
            point.e2 = 0.1
        return points

    def __point_f(self, points):
        for point in points:
            point.f = 200
        return points

    def __point_f2(self, points):
        for point in points:
            point.f = 500
        return points
