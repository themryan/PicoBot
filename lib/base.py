"""
@file base.py

@description The Base class acts as the central input and output manager for all other modules in PicoBot

@author Michael Ryan
@date {6/18/23}
"""

from output import Output
from input import Input
from display import Display
from motor_control import MotorControl
import board
import os
from HC_SR04 import HC_SR04
import alarm
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import socketpool
import wifi
from robot_modes import RobotMode

class Base:
    """
    This class acts as central control.
    
    This class contains the following objects
        output - controls publishing and screen writes
        input - controls the messages received from the MQTT connection
        sonar - the HC-SR04 distance detector
        i_am - The owner of this robot
    """

    RIGHT_MOTOR2 = board.GP16
    RIGHT_MOTOR1 = board.GP17

    LEFT_MOTOR2 = board.GP18
    LEFT_MOTOR1 = board.GP19

    HC_SR04_TRIGGER = board.GP20
    HC_SR04_ECHO = board.GP21

    # defaults
    broker = "broker.mqttdashboard.com"
    troop_id_str = "generic_troop1"
    topic_pub = "generic_troop1/chat"

    WHOAMI = 0 # default

    troop = ["Member1"]

    def __init__(self, display, wifi_connected):
        """
        Construction method for the base foundation class

        @param display the Display object
        @param wifi_connected a boolean value that is true if the wifi is connected
        """
        self._wifi_connected= wifi_connected
        print(wifi_connected)

        who_am_i_index = 0
        index = os.getenv("TROOP_INDEX")

        if index is not None:
            who_am_i_index = index

        self.WHOAMI = who_am_i_index

        troop_str_id = os.getenv["TROOP_ID"]

        if troop_str_id is not None:
          self.troop_id_str = troop_str_id

        self.topic_pub = "Troop" + self.troop_id_str + "/chat"

        troop_members = os.getenv["TROOP_MEMBERS"]

        if troop_members is not None:
          self.troop = troop_members

        if self.WHOAMI < 0 or self.WHOAMI >= len(self.troop):
            self.WHOAMI = len(self.troop) - 1

        self.i_am = self.troop[self.WHOAMI]

        broker = os.getenv["MQTT_BROKER"]
        if broker is not None:
            self.broker = broker

        self.client_id = self.i_am
        self.mqtt_server = self.broker
        self._client = None

        topic_client_id = self.client_id.replace(" ", "_")

        self.topic_ctrl = self.troop_str + "/" + topic_client_id + "_ctrl"

        self.input = Input(self._wifi_connected, self.topic_pub)

        if self._wifi_connected:
            try:
                print("Connecting")
                self._client = self.connect()
            except OSError as e:
                self.__reconnect()

        if self._wifi_connected:
            self.input.subscribe(self._client, [(self.topic_pub, 0), (self.topic_ctrl, 0)])

        self.output = Output(self._wifi_connected, self.client_id, self._client, display, self.broker, self.topic_pub)

        self.motor = MotorControl(self.LEFT_MOTOR1, self.LEFT_MOTOR2, self.RIGHT_MOTOR1, self.RIGHT_MOTOR2)

        self.sonar = HC_SR04(self.HC_SR04_TRIGGER, self.HC_SR04_ECHO)

    def connect(self):
        pool = socketpool.SocketPool(wifi.radio)
        client = MQTT.MQTT(username=self.client_id, broker=self.mqtt_server, socket_pool=pool, password="")

        # Setup the callback methods above
        client.on_connect = self.__connected
        client.on_disconnect = self.__disconnected
        client.on_message = self.__message

        client.connect()
        print("Connected to %s MQTT Broker" % (self.mqtt_server))
        return client

    def __reconnect(self):
        print("Failed to connect to the MQTT Broker. Reconnecting...")
        time.sleep(5)
        machine.reset()

    def __message(self, client, topic, message):
        msg = message
        if topic == self.topic_pub:
            client = ""
            try:
                client, msg = message.split(":")
                if client == self.client_id:
                    # Discard if from one self
                    pass
                else:
                    if msg.strip() == "Hi":
                        self.output.publish("Hi " + client)

                    self.input.received(topic, message)
            except:
                # Discard message if client not found
                msg = ""
        else:
            self.input.received(topic, message)

        print("{0}: {1}".format(topic, message))

    def __connected(self, client, userdata, flags, rc):
        print("Connected!")

    def __disconnected(self, userdata, rc):
        self.__reconnect()

    def is_connected(self):
        return self._wifi_connected


    def loop(self):
        if self._client is not None:
            self._client.loop()

    def client(self):
        return self._client





