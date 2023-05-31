class Interpreter:

    __linear = 0
    __angular = 0
    __time_ms = 0

    def __init__(self, input_file=None):

        self.COMMANDS = {
            "FWD": self.__forward,
            "REV": self.__reverse,
            "ST!": self.__stop,
            "RGT": self.__right,
            "LFT": self.__left,
            "GO!": self.__go,
        }

        self.motor_commands = []

        if input_file is not None:
            self.load_commands(input_file)

    def load_commands(self, input_file):
        for line_number, line in enumerate(input_file):
            self.__line_number = line_number
            self.__parser(line)

    def __error(self, input_str):
        print("Error on {self.__line_number}: {input_str}")

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
