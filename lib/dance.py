import base
import os
from interpreter import Interpreter
import time

class Dance:
    """
    This class opens a file specified in settings.toml's 'DANCE_FILE' setting
    """
    def __init__(self, base):
        self._base = base

        dance_instructions = os.getenv("DANCE_FILE")

        if dance_instructions is None:
            dance_instructions = "dancing.txt"

        self.dance_instructions = dance_instructions

        file = None

        self._next_line = True

        self._end_time = 0

        self._base.motor.velocities(0, 0)

        try:
            file = open(self.dance_instructions, "r")
        except Exception as e:
            print("Error in opening file")
            print("ERROR: " + str(e))
            exit()

        self.__interpreter = Interpreter(file)
        file.close()

        self._base.output.screen("I'm Dancing", 0, 16, 1)
        self._base.output.screen("Chat: ", 0, 30, 2)
        self._base.motor.set_accel_scale(20)

    def loop(self):
        now = time.monotonic_ns()
        if self.__interpreter is not None and len(self.__interpreter.motor_commands) > 0:
            if self._next_line:
                print(self.__interpreter.motor_commands)

                instruction = self.__interpreter.motor_commands.pop(0)
                if len(instruction) == 3:
                    self._end_time = now + instruction[2]*1000000
                    self._base.motor.velocities(instruction[0], instruction[1])
                    self._next_line = False

        if now > self._end_time:
            if len(self.__interpreter.motor_commands) == 0:
                self._base.motor.velocities(0, 0)
                self._base.output.screen("I've Stopped Dancing", 0, 16, 1)
            else:
                self._end_time = now + self._end_time

            self._next_line = True

        distance = self._base.sonar.distance()

        messages = self._base.input.messages()
        if messages != "":
            self._base.output.screen("Chat: " + messages, 0, 30, 2)

        self._base.motor.drive()




