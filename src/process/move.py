import re
import math
from process import Process
from process import Point


class Move(Process):

    """
    Example:

        ''' move
            X: 80 mm
            Y: 40 mm
            Z: 80 mm
            E: 10 mm
            Feedrate: 800 mm/min
        '''
    """

    params_rules = {
        # Key:      [Unit,       Required,      Default Value]
        'X':        ['length',   False,         None],
        'Y':        ['length',   False,         None],
        'Z':        ['length',   False,         None],
        'E':        ['length',   False,         None],
        'Feedrate': ['feedrate',   False,       500]
    }

    def points(self):
        point_list = []

        if self.feedrate is not None:
            point_list.append(Point(f=self.feedrate))

        point_list.append(Point(x=self.x, y=self.y, z=self.z, e1=self.e))

        return point_list
