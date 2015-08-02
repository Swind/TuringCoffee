from process import Process
from process import Command


class Wait(Process):

    """
    Example:

        ''' wait
            Time: 30s
        '''

    """

    params_rules = {
        'Time': ['time', False, None],
        'Temperature': ['temperature', False, None],
    }

    def points(self):
        return [Command('Wait', self.time)]
