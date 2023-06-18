"""
@file remote.py

@description This file supports the remote control mode of the robot

@author Michael Ryan
@date {6/18/23}
"""

import base
import wifi
from interpreter import Interpreter
import time

class Remote:
    """
    Class for connecting to remove MQTT site for robot control
    """
    def __init__(self, base):
        time.sleep(0.1)
        self._base = base
        self._interpreter = Interpreter()

        self._base.output.screen("Remote", 0, 16, 1)
        self._end_time = 0
        self._next_line = True

        self._base.motor.set_accel_scale(30)

    def loop(self):
        """
        """
        now = time.monotonic_ns()
        commands = self._base.input.messages(self._base.topic_ctrl)

        if commands != "":
            # if new commands append to motor commands
            self._interpreter.load_commands(commands.splitlines())

        motor_commands = self._interpreter.motor_commands

        if self._end_time < now:
            self._end_time = 0
            if len(motor_commands) > 0:
                print(len(motor_commands))
                if self._next_line:
                    while True:
                        instruction = self._interpreter.motor_commands.pop(0)
                        print(instruction)
                        if len(instruction) > 0:
                            self._end_time = now + instruction[2]*1000000
                            self._base.motor.velocities(instruction[0], instruction[1])
                            self._next_line = False
                            break
                        elif len(motor_commands) == 0:
                            break
            else:
                if len(self._interpreter.motor_commands) == 0:
                    self._base.motor.velocities(0,0)
                    self._end_time = 0
        else:
            self._next_line = True


        self._base.motor.drive()
