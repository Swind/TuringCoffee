import pid_controller
from utils import json_config
from utils import channel

class Server(object):
    def __init__(self):
        # Read Config
        self.config = json_config.parse_json("config.json")

        # Create PID controller
        self.pid_controller = pid_controller.PIDController(self.config)

        # That other process can subscribe the pid controller status
        self.pub_channel = channel.Channel(self.config["HeaterServer"]["Publish_Socket_Address"], "Pub", True)

        # Receive the pid controller command
        self.cmd_channel = channel.Channel(self.config["HeaterServer"]["Command_Socket_Address"], "Pair", True)

    def __pid_controller_observer(self, *pid_status):
        self.publish_pid_status(*pid_status)

    def start(self):
        # Start pid controller thread
        self.pid_controller.start()

        # Add observer to publish pid status
        self.pid_controller.add_observer(self.__pid_controller_observer)

        # The main thread will receive and set the pid parameters by nanomsg
        self.receive_pid_parameters()

    # ============================================================================================================
    #
    #   nanomsg API
    #
    # ============================================================================================================
    def publish_pid_status(self, cycle_time, duty_cycle, set_point, temperature):
        """
        Publish pid status:
        e.g

        {
            "cycle_time": 5,
            "duty_cycle": 70,
            "set_point": 80,
            "temperature": 26.53
        }
        """
        print "Publish cycle_time:{}, duty_cycle:{}, set_point:{}".format(cycle_time, duty_cycle, set_point, temperature)
        self.pub_channel.send({"cycle_time": cycle_time, "duty_cycle": duty_cycle, "set_point": set_point, "temperature": temperature})

    def receive_pid_parameters(self):
        """
        Receive pid parameters:
        e.g
        {
            "cycle_time": 1,
            "k": 44,
            "i": 165,
            "d": 4,
            "set_point": 80
        }
        """
        # The main thread will handle the command socket
        while(True):
            cmd = self.cmd_channel.recv()

            self.pid_controller.set_params(cmd["cycle_time"], cmd["k"], cmd["i"], cmd["d"], cmd["set_point"])


if __name__ == "__main__":
    server = Server()
    server.start()
