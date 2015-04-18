import msgpack

from nanomsg import (
    PUB,
    SUB,
    SUB_SUBSCRIBE,
    PAIR,
    DONTWAIT,
    Socket,
    NanoMsgAPIError,
    EAGAIN
)


class Channel(object):

    type_map = {
        'Sub': SUB,
        'Pub': PUB,
        'Pair': PAIR
    }

    def __init__(self, address, channel_type, is_server):
        self.__socket = Socket(self.type_map[channel_type])

        if is_server:
            self.__socket.bind(address)
        else:
            self.__socket.connect(address)

            if channel_type == 'Sub':
                self.__socket.set_string_option(SUB, SUB_SUBSCRIBE, '')

    def recv(self, blocking=True):

        if blocking:
            result = self.__socket.recv()
        else:
            try:
                result = self.__socket.recv(flags=DONTWAIT)
            except NanoMsgAPIError as error:
                if error.errno == EAGAIN:
                    return None

        return msgpack.unpackb(result)

    def send(self, msg):
        return self.__socket.send(msgpack.packb(msg))
