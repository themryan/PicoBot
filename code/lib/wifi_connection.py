"""
@file wifi_connection.py

@description This file supports the Raspberry Pi Pico W's wifi connection

@author Michael Ryan
@date {6/18/23}
"""

import wifi
import os
import time
import microcontroller

class WifiConnection:
    """
    This class connects to the SSIDs listing in the settings.toml file.

    It searches for SSDI0 first and if it has an issue connecting will try SSID1 next
    and will continue to SSDIx (10 max) until it has a connection.
    """

    def __init__(self, display):
        """
        Constructor method of the WifiConnection class

        @param display Display object
        """
        self.connected = False
        self.ssid_count = 0
        self._continue_trying = True

        self._display = display

        while self._continue_trying:
            self.connect_with_new_id()


    def reset_on_error(self, delay, error):
        """
        Resets the code after a specified delay, when encountering an error in connecting
        """
        print("Error:\n", str(error))

        wifi.radio.enabled = False
        time.sleep(0.01)
        wifi.radio.enabled = True

        if self.ssid_count < 10:
            self.ssid_count = self.ssid_count + 1
        else:
            reset_on_connection_issue = os.getenv("RESET_ON_WIFI_FAIL")
            if reset_on_connection_issue is None or reset_on_connection_issue == 1:
                print("Resetting microcontroller in %d seconds" % delay)
                time.sleep(delay)
                microcontroller.reset()

            self._continue_trying = False


    def connect(self):
        """
        Attempt to connect to the wifi with SSID and password

        @param ssid SSID of the intended wifi network
        @param password Password for the intended SSID
        """
        try:
            wifi.radio.connect(self.wifi_id, self.wifi_pwd)
            print("Connected to " + self.wifi_id)
            self.connected = True
            self._display.text("Connected!", 0, 8, 0)
            print("Connected!")
            self._continue_trying = False
        # any errors, reset MCU
        except Exception as e:  # pylint: disable=broad-except
            print("Failed to connect to " + self.wifi_id)
            self.reset_on_error(10, e)
            self.connected = False

    def connect_with_new_id(self):
        """
        Will search settings.toml for the next defined Wifi SSID
        """
        wifi_id_str = "WIFI_SSID" + str(self.ssid_count)
        wifi_pwd = wifi_id_str + "_PWD"
        self.wifi_id = os.getenv(wifi_id_str)
        if self.wifi_id is None:
            error_text = "Could not find " + wifi_id_str
            self._display.text(error_text, 0, 8, 0)
            self.reset_on_error(1, error_text)
        else:
            self.wifi_pwd = os.getenv(wifi_pwd)

            self._display.text("Connecting to " + self.wifi_id, 0, 8, 0)
            self.connect()


    def get_ip(self):
        """
        Will return the IP address of the connection
        """
        return wifi.radio.ipv4_address
