import paho.mqtt.client as mqtt
import json


def is_callback(channels):
    def decorated(func):
        def wraps(*args, **kwargs):
            if args[0] == 'channels':
                return channels
            else:
                response = func(*args, **kwargs)
                return response
        return wraps
    return decorated


@is_callback(["google/mail", "google/people"])
def callback_test2(token):
    print("callback from test2; token : {}".format(token))


@is_callback(["google/mail"])
def callback_test1(token):
    print("callback from test1; token : {}".format(token))


def dispatch(message, callbacks):
    """
    Given a message, calls every callback that matches the message topic
    """
    for callback in callbacks:
        if message.topic in callback("channels"):
            callback(json.loads(message.payload)["token"])


class Service:

    def __init__(self, callbacks, host, port):
        self.client = mqtt.Client()
        self.callbacks = callbacks
        self.host = host
        self.port = port

        self.client.connect(host, port)

        to_subscribe = []
        for callback in self.callbacks:
            for channel in callback("channels"):
                to_subscribe.append(channel)

        # subscibing to all relevant channels

        [self.client.subscribe(channel) for channel in list(set(to_subscribe))]

        # dispatching the messages to the right callback(s)

        self.client.on_message = lambda client, userdata, msg: dispatch(
            msg, self.callbacks)

        self.client.loop_forever()

if __name__ == "__main__":
    s = Service([callback_test2, callback_test1], "127.0.0.1", 1883)
