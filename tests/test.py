import time
import msgpack

from nanomsg import (
    SUB,
    PAIR,
    DONTWAIT,
    SUB_SUBSCRIBE,
    Socket
)

with Socket(PAIR) as s2:
    s2.connect("ipc:///tmp/cmd_pid_controller")
    payload = {
        "cycle_time": 5,
        "k": 44,
        "i": 165,
        "d": 4,
        "set_point": 80
    }
    s2.send(msgpack.packb(payload))

with Socket(SUB) as s1:
    s1.connect("ipc:///tmp/pub_pid_controller")
    s1.set_string_option(SUB, SUB_SUBSCRIBE, '')

    while (True):
        resp = s1.recv()
        print msgpack.unpackb(resp)

        time.sleep(1)
