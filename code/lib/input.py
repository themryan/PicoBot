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
        """
        Pop and return the last message off of the queue
        """
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
        """
        Push message to queue

        @param message A str object to be retained by queue
        """
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
        """
        Constructor for the Input class 

        @param wifi_connected A boolean that is True if wifi is connected
        @param topic_pub The default topic
        """
        self.__wifi_connected = wifi_connected
        self.__topic_pub = topic_pub

        self.__messages = {}

    def subscribe(self, client, topic = None):
        """
        Subscribe to a topic

        @param client The MQTT Client object
        @param topic The optional topic to subscribe to 
                     if None the default topic will be used
        """
        if self.__wifi_connected:
            if topic is None:
                topic = self.__topic_pub
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
        """"
        Unsubscribe to a topic

        @param client MQTT Client object
        @param topic Topic to unsubscribe from
        """
        if self.__wifi_connected:
            try:
                client.unsubscribe(self.__topic_pub)
            except Exception as e:
                print("Failed to unsubscribe")
                print(e)


    def received(self, topic, message):
        """
        Push the message into the topic's message queue

        @param topic Topic's queue to push the message to
        @param message Message to push to queue 
        """
        self.__messages[topic].push(message)


    def messages(self, topic=None):
        """
        Returns any received messages

        @param topic Optional topic queue to receive messages from
                     If None will retrieve messages from default topic queue
        """
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

