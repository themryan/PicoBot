"""
@file HC_SR04.py

@description This file provides non-blocking support for the HC-SR04 device

@author Michael Ryan
@date {6/18/23}
"""
import time
import pulseio
import digitalio

class HC_SR04:
    """
    @class Interface to a HC-SR04 sonar device
    """
    MAX_TRIGGER_TIME_LEN = 10000  # ns

    START_TRIGGER = 0
    END_TRIGGER = 1
    WAITING_FOR_ECHO = 2

    ECHO_DURATION = 3
    PROCESS = 4

    def __init__(self, trigger_pin, echo_pin):
        """
        Constructor method of the HC_SR04 device interface

        @param trigger_pin The gpio pin connected to the HC-SR04 trigger
        @param echo_pin The gpio pin connected to the HC-SR04 echo
        """
        self._echoes = pulseio.PulseIn(echo_pin, idle_state=False)
        self._echoes.pause()
        self._trigger = digitalio.DigitalInOut(trigger_pin)
        self._trigger.direction = digitalio.Direction.OUTPUT
        self._trigger.value = True
        self._start_trigger()
        self._distance = -1

    def _start_trigger(self):
        """
        Start the trigger pulse
        """
        self.__state = self.START_TRIGGER
        self._start_time = time.monotonic_ns()
        self._timeout_count = 0
        self._trigger.value = True
        self._echoes.pause()

    def __end_trigger(self):
        """
        End the trigger pulse and start wait for echoes pulse
        """
        self._state = self.END_TRIGGER
        self._trigger.value = False
        self._echoes.clear()
        self._echoes.resume()

    def __get_distance(self):
        """
        Returns the last distance measured and advances the device driver state
        """
        if self.__state == self.START_TRIGGER:
            if (time.monotonic_ns() - self._start_time) > self.MAX_TRIGGER_TIME_LEN:
                self.__end_trigger()
        elif self.__state == self.END_TRIGGER:

            if len(self._echoes) >= 1:

                self._echoes.pause()
                duration = self._echoes[0]
                self._echoes.clear()
                self._distance = duration * 17165 / 1000000
                self._start_trigger()
            else:
                self._timeout_count = self._timeout_count + 1

        if self._timeout_count > 30:
            self._distance = -1
            self._start_trigger()

        return self._distance

    def distance(self):
        """
        Returns the last distance measured by the HC-SR04 or -1 if not responding

        Needs to be polled continuously to keep device driver state advancing
        """
        return self.__get_distance()

