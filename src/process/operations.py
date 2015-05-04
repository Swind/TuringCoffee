from process import Command
from process import Process


class Operations(Process):

    """
    Example:

        ''' operations
            Command: Home
            Command: Refill START
        '''
    """

    params_rules = {
        # Key:      [Unit,       Required,      Default Value]
        'Command':  [None,       True,          None]
    }

    def points(self):
        result = [Command(self.command, None)]
        return result
