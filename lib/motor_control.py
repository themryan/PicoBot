"""
@file motor_control.py

@description This file provides an interface to the adafruit_motor module

@author Michael Ryan
@date {6/18/23}
"""

from adafruit_motor import motor
import pwmio

class MotorControl:
    """
    Class that manages the motor via the HW-627 DRV8833 H-bridge driver
    """
    # Arbitrarily chose a frequency of 100000 Hz that seemed to work best for our motors
    # This may need to be adjusted for different motors
    frequency = 100000

    MAX_PWM = 65535
    MAX_INPUT = 100
    MIN_VELOCITY_THRESHOLD_DIFF = 0.1

    def __init__(self, motor_a_1, motor_a_2, motor_b_1, motor_b_2):
        """
        Four parameters are
            pin for right motor power line 1
            pin for right motor power line 2
            pin for left motor power line 1
            pin for left motor power line 2
        """
        pwm1_a = pwmio.PWMOut(motor_a_1, frequency=self.frequency, duty_cycle=0)
        pwm2_a = pwmio.PWMOut(motor_a_2, frequency=self.frequency, duty_cycle=0)
        pwm1_b = pwmio.PWMOut(motor_b_1, frequency=self.frequency, duty_cycle=0)
        pwm2_b = pwmio.PWMOut(motor_b_2, frequency=self.frequency, duty_cycle=0)

        self._motor_a = motor.DCMotor(pwm1_a, pwm2_a)
        self._motor_b = motor.DCMotor(pwm1_b, pwm2_b)

        self._motor_a.throttle = None
        self._motor_b.throttle = None

        self._motor_a.decay_mode = motor.SLOW_DECAY
        self._motor_b.decay_mode = motor.SLOW_DECAY

        self.__linear = 0.0
        self.__angular = 0.0
        self.__prev_pwm1 = 0.0
        self.__prev_pwm2 = 0.0
        self.__last_time = 0

        self.__active_velocities = [0.0, 0.0]
        self.__cmd(0, 0)

        self.__accel_scale = 100

    def velocities(self, linear, angular):
        """
        Input the desired angular and linear velocities

        @param linear Linear velocity value
        @param angular Angular velocity value
        """
        if linear > self.MAX_INPUT or linear < -self.MAX_INPUT:
            print("Linear velocity must be between {1self.MAX_INPUT} and {self.MAX_INPUT}.")

            if linear < 0:
                linear = -self.MAX_INPUT
            else:
                linear = self.MAX_INPUT

        if angular > 100 or angular < -100:
            print("Linear velocity must be between {-self.MAX_INPUT} and {self.MAX_INPUT}")

            if angular < 0:
                angular = -self.MAX_INPUT
            else:
                angular = self.MAX_INPUT

        self.__linear = linear/self.MAX_INPUT
        self.__angular = angular/self.MAX_INPUT

    def __cmd(self, duty1, duty2):
        self._motor_a.throttle = duty1
        self._motor_b.throttle = duty2

    def drive(self):
        """
        Drive the robot with the last passed velocities
        """
        pwm1  = 0.0
        pwm2 = 0.0

        commanded_linear = self.__linear
        commanded_angular = self.__angular

        pwm1 = commanded_angular + commanded_linear
        pwm2 = commanded_angular - commanded_linear

        if pwm1 >= 1.0 or pwm1 <= -1.0:

            if pwm1 < 0:
                # 1.0 and -1.0 appear to overload system
                # Limit to 900
                pwm1 = -0.90
            else:
                pwm1 = 0.90

        if pwm2 >= 1.0 or pwm2 <= -1.0:
            # 1.0 and -1.0 appear to overload system
            # Limit to 900
            if pwm2 < 0:
                pwm2 = -0.90
            else:
                pwm2 = 0.90

        diff_pwm1 = pwm1 - self.__active_velocities[0]
        diff_pwm2 = pwm2 - self.__active_velocities[1]

        abs_diff_pwm1 = abs(diff_pwm1)
        abs_diff_pwm2 = abs(diff_pwm2)

        abs_diff_max = abs_diff_pwm1
        if abs_diff_pwm2 > abs_diff_max:
            abs_diff_max = abs_diff_pwm2

        if abs(diff_pwm2) > self.MIN_VELOCITY_THRESHOLD_DIFF:
            dividing_factor = self.__accel_scale
            if abs_diff_max < 0.5:
                dividing_factor = dividing_factor/2

            increment_pwm1 = (diff_pwm1/dividing_factor)
            increment_pwm2 = (diff_pwm2/dividing_factor)

            new_pwm1 = self.__active_velocities[0] + increment_pwm1
            new_pwm2 = self.__active_velocities[1] + increment_pwm2

            if abs(pwm1 - new_pwm1) < abs(increment_pwm1):
                new_pwm1 = pwm1
            if abs(pwm2 - new_pwm2) < abs(increment_pwm2):
                new_pwm2 = pwm2

            pwm1 = new_pwm1
            pwm2 = new_pwm2

        self.__active_velocities = [pwm1, pwm2]

        self.__cmd(pwm1, pwm2)

    def set_accel_scale(self, accel_scale):
        self.__accel_scale = accel_scale

    @property
    def throttle(self):
        """
        Return the throttle values for motor a and motor b
        """
        return self._motor_a.throttle, self._motor_b.throttle

