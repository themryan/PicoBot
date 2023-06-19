"""
@file output.py

@description This file provides an interface to the MQTT advertised topics and display

@author Michael Ryan
@date {6/18/23}
"""

from display import Display
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import socketpool
from robot_modes import RobotMode
from display import Display
import time
import board
import busio

class Cursor:
    x = 0
    y = 0

class Output:
    """
    This class manages all outputs screen and MQTT publishing
    """
    mqtt_server = "broker.mqttdashboard.com"
    client_id = ""
    topic_pub = ""

    def startup_screen(self, id):
        """
        Startup screen for the robot

        @param id ID text to display in the startup screen
        """
        self.display.fill(128, 64, True, 0)
        self.display.fill(120, 56, False, 1, 4, 4)

        time.sleep(0.01)
        self.display.text("Troop " + id, 32, 24, 2)
        time.sleep(0.01)
        self.display.text("Robot", 50, 40, 3)
        time.sleep(0.01)

    def debug(self, text, x=None, y=None):
        """
        Displays the desired text to debug mode screen
        """
        if RobotMode.mode == RobotMode.DEBUG:
            if x is None:
                x = self._cursor.x
            if y is None:
                y = self._cursor.y

            self.display.text(text, x, y)


    def publish(self, txt, topic=None):
        """
        Publishes the text supplied by txt to the default or supplied topic

        @param txt String with the desired message to be published
        @param topic Optional string with the topic to publish to
        """
        if topic is None:
            topic = self.topic_pub

        if self._wifi_connected:
            if self.__client is not None:
                msg = self.client_id + ": " + txt
                self.__client.publish(topic, msg)

    def __init__(self, wifi_connected, client_id, client, display, broker=None, topic_pub=None):
        """
        Constructor for Output class

        @param wifi_connected Boolean is True when wifi is connected
        @param client_id Client ID for the MQTT connection
        @param client Client object of the MQTT connection
        @param display Display object
        @param broker Optional broker ID (text)
        @param topic_pub Optional topic to publish to
        """
        self.display = display
        self._wifi_connected = wifi_connected

        if broker is not None:
            self.mqtt_server = broker

        if topic_pub is not None:
            self.topic_pub = topic_pub

        self.__client = client
        self.client_id = client_id
        if self._wifi_connected:
            self.publish("Hi")

        self._cursor = Cursor()

    def out(self, text, x=None, y=None):
        """
        Dipslay text on the screen

        @param text Message to display
        @param x Optional horizontal position of the upper left corner of the text rectangle
        @param y Optional vertical position of the upper left corner of the text rectangle
        """
        self.display.text(text, self._cursor.x, self._cursor.y)

    def out_all(self, text, x=None, y=None):
        """
        Dipslay text on the screen and published text to default topic

        @param text Message to display
        @param x Optional horizontal position of the upper left corner of the text rectangle
        @param y Optional vertical position of the upper left corner of the text rectangle
        """
        x, y = self.__check_xy(x, y)

        self.display.text(text, x, y, 0)

        self.publish(text)

    def __check_xy(self, x, y):
        if x is None:
            x = self._cursor.x
        if y is None:
            y = self._cursor.y

        return x, y

    def screen(self, text, x=None, y=None, layer=None, scale=1, color=True):
        """
        Raw write of text to screen 

        @param text Message to display
        @param x Optional horizontal position of the upper left corner of the text rectangle
        @param y Optional vertical position of the upper left corner of the text rectangle
        @scale Scale of the font
        @color True if positive pixels, False if inverted
        """
        x, y = self.__check_xy(x, y)

        self.display.text(text, x, y, layer, scale, color)

    def erase(self):
        """
        Clear the screen
        """
        self.display.clear()

    def debug(self, text):
        """
        Debug output 

        @param text Text to output to screen
        """
        self.out(text)
