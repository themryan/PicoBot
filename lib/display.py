"""
@file display.py

@description This provides a general wrapper to the adafruit_displayio_ssd1306 library for outputting to the screen

@author Michael Ryan
@date {6/18/23}
"""

import displayio
import busio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import terminalio
import time

class DebugScreen:
    """
    Writes all outputs to the screen for debugging
    """
    def __init__(self, display):
        self._wifi_info = ""
        self._sonar = ""
        self._motor = ""
        self._mqtt = ""

        self._wifi_info_text = "Wifi: "
        self._sonar_text = "Sonar: "
        self._motor_text = "Motor: "
        self._mqtt_text = "MQTT: "
        self._wifi_info_pos = [0, 4]
        self._motor_pos = [0, 20]
        self._sonar_pos = [0, 36]
        self._mqtt_pos = [0, 54]

        self._wifi_info_layer = 0
        self._mqtt_layer = 1
        self._sonar_layer = 2
        self._motor_layer = 3

        self._display = display

        self._display.clear()

        self.__update()

    @property
    def motor(self):
        return self._motor

    @motor.setter
    def motor(self, info: str):
        self._motor = info
        self.__update()

    @property
    def wifi_info(self):
        return self._wifi_info

    @wifi_info.setter
    def wifi_info(self, info: str):
        self._wifi_info = info
        self.__update()

    @property
    def sonar(self):
        return self._sonar

    @sonar.setter
    def sonar(self, sonar: str):
        self._sonar = sonar
        self.__update()

    @property
    def channel(self):
        return self._mqtt

    @channel.setter
    def channel(self, channel: str):
        self._mqtt = channel
        self.__update()


    def __update(self):
        self._display.text(self._wifi_info_text + self._wifi_info,
                            self._wifi_info_pos[0], self._wifi_info_pos[1], self._wifi_info_layer)

        self._display.text(self._mqtt_text + self._mqtt,
                            self._mqtt_pos[0], self._mqtt_pos[1], self._mqtt_layer)

        self._display.text(self._sonar_text + self._sonar,
                            self._sonar_pos[0], self._sonar_pos[1], self._sonar_layer)

        self._display.text(self._motor_text + self._motor,
                            self._motor_pos[0], self._motor_pos[1], self._motor_layer)


class Display:
    """
    Manages the interface to the OLED display
    """
    throttle_threshold = 100000

    def __init__(self, sda_pin, scl_pin):

        displayio.release_displays()
        i2c = busio.I2C(scl=scl_pin, sda=sda_pin)
        display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
        display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

        self.__group = displayio.Group()
        self.__layer = 0
        display.show(self.__group)
        self._last_published_time = 0

    def __check_throttle(self):
        now = time.monotonic_ns()
        if now - self._last_published_time > self.throttle_threshold:
            self._last_published_time = now
            return True

        return False

    def fill(self, width, height, is_on, layer=None, x=0, y=0):
        if self.__check_throttle():
            color_bitmap = displayio.Bitmap(width, height, 1)

            # Monochromatic Display
            color_palette = displayio.Palette(1)
            color_palette[0] = 0xFFFFFF # White

            if not is_on:
                color_palette[0] = 0x000000  # Black

            fill = displayio.TileGrid(color_bitmap,
                                      pixel_shader=color_palette, x=x, y=y)

            if layer is None:
                layer = len(self.__group)

            if layer < 0:
                layer = 0

            if layer >= len(self.__group):
                self.__group.append(fill)
            else:
                self.__group[layer] = fill


    def text(self, text, x, y, layer=None, scale = 1, color=True):
        if self.__check_throttle():
            foreground_color = 0x0FFFFFF
            if not color:
                foreground_color = 0

            text_area = label.Label(terminalio.FONT, scale=scale, color=foreground_color, text=text, x=x, y=y)

            if layer is None:
                layer = len(self.__group)

            if layer < 0:
               layer = 0

            if layer >= len(self.__group):
                self.__group.append(text_area)
            else:
                self.__group[layer] = text_area


    def clear(self):
        while len(self.__group) > 0:
            self.__group.pop()
