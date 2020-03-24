import json
import os

import paho.mqtt.client as mqtt
import redis

from helpers.redis_helpers import getData, setData


def is_callback(channels):
    def wrapper(func):
        setattr(func, "channels", channels)
        return func
    return wrapper


def dispatch(message, callbacks):
    """
    Given a message, calls every callback that matches the message topic
    """
    try:
        for callback in callbacks:
            if message.topic in callback.channels:
                res = callback(json.loads(
                    message.payload.decode("utf-8"))["token"])
                print(res)
    except Exception as e:
        print(e)


class Service:

    def __init__(self, callbacks):
        try:
            # self.redis = redis.Redis(os.getenv("REDIS_HOST", "127.0.0.1"),
            #                          int(os.getenv("REDIS_PORT", 6379)))

            self.mqtt = mqtt.Client()
            self.mqtt.connect(os.getenv("MQTT_HOST", "localhost"),
                              int(os.getenv("MQTT_PORT", 1883)))

            self.callbacks = callbacks

            to_subscribe = []
            for callback in self.callbacks:
                for channel in callback.channels:
                    to_subscribe.append(channel)

            # subscibing to all relevant channels

            [self.mqtt.subscribe(channel)
             for channel in list(set(to_subscribe))]

            # dispatching the messages to the right callback(s)

            self.mqtt.on_message = lambda client, userdata, msg: dispatch(
                msg, self.callbacks)

            self.mqtt.loop_forever()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    # print(os.getenv("MQTT_PORT"))

    @is_callback(["hey"])
    def f(x):
        return "bla"

    s = Service([f])
