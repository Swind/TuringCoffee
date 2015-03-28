from process import Command
from process import Process

class Operations(Process):
    """
    Example:

        ''' operations
            Command: Home
            Command: Refill
            Command: Wait 30s
        '''
    """

    params_rules = {
        # Key:      [Unit,       Required,      Default Value]
        "Command":  [None,       True,          None]
    }

    def points(self):
        result = map(lambda item: Command(item, None), self.command)
        return result

