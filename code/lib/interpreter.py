"""
@file interpreter.py

@description This file provides support for the 

@author Michael Ryan
@date {6/18/23}
"""

class Interpreter:
    """
    @description 
    The interpreter will read the following text-based commmands

    FWD
    REV
    ST!
    RGT
    LFT
    GO!

    and will provide a corresponding motor command.

    @param an optional input_file containing commands

    """
    __linear = 0
    __angular = 0

    def __init__(self, input_cmds=None):
        """
        Constructor fo the Interpreter class

        @param input_file Optional list of commands
        """
        self.COMMANDS = {
            "FWD": self.__forward,
            "REV": self.__reverse,
            "ST!": self.__stop,
            "RGT": self.__right,
            "LFT": self.__left,
            "GO!": self.__go,
        }

        self.motor_commands = []

        if input_cmds is not None:
            self.load_commands(input_cmds)

    def load_commands(self, input_cmds):
        """
        Load the list of commands in input_cmds into the parser

        @param input_cmd Newline delineated list of commands for the parser
        """
        for line_number, line in enumerate(input_cmds):
            self.__line_number = line_number
            self.__parser(line)

    def __error(self, input_str):
        print("Error on {}: {}", self.__line_number, input_str)

    def __parser(self, input_line):
        instruction = input_line[0:3]
        if instruction in self.COMMANDS:
            self.COMMANDS[instruction](input_line)

    def __forward(self, input_line):
        if input_line[3:].isdigit:
            self.__linear = self.__linear + int(input_line[3:])
        else:
            self.__error(input_line)

    def __reverse(self, input_line):
        if input_line[3:].isdigit:
            self.__linear = self.__linear - int(input_line[3:])
        else:
            self.__error(input_line)

    def __right(self, input_line):
        input_line.strip()
        if input_line[3:].isdigit:
            self.__angular = self.__angular - int(input_line[3:])
        else:
            self.__error(input_line)

    def __left(self, input_line):
        input_line.strip()
        if input_line[3:].isdigit:
            self.__angular = self.__angular + int(input_line[3:])
        else:
            self.__error(input_line)

    def __stop(self, input_line):
        time_ms = 0
        if input_line != "":
            input_line.strip()
            if input_line[3:].isdigit:
                time_ms = int(input_line[3:])
        self.__linear = 0
        self.__angular = 0

        self.motor_commands.append([self.__linear, self.__angular, time_ms])

    def __go(self, input_line):
        input_line.strip
        if input_line[3:].isdigit:
            time_ms = int(input_line[3:])
            self.motor_commands.append([self.__linear, self.__angular, time_ms])
        else:
            self.__error(input_line)

        self.__linear = 0
        self.__angular = 0
