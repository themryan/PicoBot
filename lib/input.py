"""
@file input.py

@description This file processes all inputs from the MQTT server and stores them in a ring buffer 

@author Michael Ryan
@date {6/18/23}
"""

import adafruit_minimqtt.adafruit_minimqtt as MQTT
from output import Output

class SimpleQueue:
    """
    Simple ring buffer
    """
    def __init__(self, size):
        self._size = size
        self._queue = [[""]]*size

        self._index_in = 0
        self._index_out = 0

    def pop(self):
        # Take them from the front
        msg = None
        index = self._index_out
        if index != self._index_in:
            self._index_out = self._index_out + 1

            if self._index_out >= self._size:
                self._index_out = 0

            msg = self._queue[index]
            self._queue[index] = ""

        return msg

    def push(self, message: str):
        self._queue[self._index_in] = message
        print(self._queue)
        self._index_in = self._index_in + 1
        if self._index_in >= self._size:
            self._index_in = 0

        if self._index_in == self._index_out:
            self._index_out = self._index_out + 1
            if self._index_out >= self._size:
                self._index_out = 0




class Input:
    """
    Class for managing inputs from subscriptions
    """

    def __init__(self, wifi_connected, topic_pub):

        self.__wifi_connected = wifi_connected
        self.__topic_pub = topic_pub

        self.__messages = {}

    def subscribe(self, client, topic = None):

        if self.__wifi_connected:
            if topic is None:
                topic = self.topic_pub
            try:
                if isinstance(topic, str):
                    print("Subscribing to " + topic)
                else:
                    for t in topic:
                        print("Subscribing to " + t[0])
                client.subscribe(topic)
                if isinstance(topic, str):
                    self.__messages[topic] = SimpleQueue(5)
                else:
                    for t in topic:
                        self.__messages[t[0]] = SimpleQueue(5)
            except Exception as e:
                print("Failed to subscribe")
                print(e)

    def unsubscribe(self, client, topic):
        if self.__wifi_connected:
            try:
                client.unsubscribe(self.topic_pub)
            except Exception as e:
                print("Failed to unsubscribe")
                print(e)


    def received(self, topic, message):
        self.__messages[topic].push(message)


    def messages(self, topic=None):
        ret_str = ""
        if topic is None:
            topic = self.__topic_pub

        if topic in self.__messages:
            message = self.__messages[topic].pop()
            while message is not None:
                print("Message Received: " + message)
                ret_str = ret_str + "\n" + message
                message = self.__messages[topic].pop()

        return ret_str

