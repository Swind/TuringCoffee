from process import Process
from process import Command


class Heat(Process):

    """
    Example:

        ''' heat
            Water Tank: 70 degress Celsius
        '''

        cmd can be [home, refill]
    """

    params_rules = {
        'Water Tank': ['temperature', False, None],
        'Wait': ['temperature', False, None],
    }

    def points(self):
        return [Command('Heat', self.water_tank)]
