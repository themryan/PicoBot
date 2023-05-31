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
    This class manages all outputs screen or internet
    """
    mqtt_server = "broker.mqttdashboard.com"
    client_id = ""
    topic_pub = ""

    def startup_screen(self, id):
        self.display.fill(128, 64, True, 0)
        self.display.fill(120, 56, False, 1, 4, 4)

        time.sleep(0.01)
        self.display.text("Troop " + id, 32, 24, 2)
        time.sleep(0.01)
        self.display.text("Robot", 50, 40, 3)
        time.sleep(0.01)

    def debug(self, text, x=None, y=None):
        if RobotMode.mode == RobotMode.DEBUG:
            if x is None:
                x = self._cursor.x
            if y is None:
                y = self._cursor.y

            self.display.text(text, x, y)


    def publish(self, txt, topic=None):
        if topic is None:
            topic = self.topic_pub

        if self._wifi_connected:
            if self.__client is not None:
                msg = self.client_id + ": " + txt
                self.__client.publish(topic, msg)

    def __init__(self, wifi_connected, client_id, client, display, broker=None, topic_pub=None):
        self.display = display
        self._wifi_connected = wifi_connected

        # self._cursor = Cursor()

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
        self.display.text(text, self._cursor.x, self._cursor.y)

    def out_all(self, text, x=None, y=None):
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
        x, y = self.__check_xy(x, y)

        self.display.text(text, x, y, layer, scale, color)

    def erase(self):
        self.display.clear()

    def debug(self, text):
        self.out(text)
