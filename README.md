# PicoBot
by Michael Ryan 
Updated 6/18/23

## License

PicoBot retains the MIT license.  You may modify, update, and distribute this software as long as the references to the original authors are retained.  PicoBot is intended as-is and does not offer any guarantee or support. 

## Introduction

PicoBot is a CircuitPython-based multi-functional robot project intended for a Raspberry Pi Pico W.  This project was originally intended to be a learning platform for a Girl Scout troop.  It is intended to be a group project with each participant building their own mobile robot.  Each participant's robot will then be able to communicate with one another over wiFi.  The communication consists mostly of just an introduction of each participant's robot to one another, a positive greeting from each active robot, and a statement of what each robot is doing.  This was intended to highlight the collaborative nature of the project and to add an extra element of fun.  

PicoBot provides a mutlifunctional aspect to each robot.  Allowing each participant to choose to run their robot in one of the following states:

#### **Dance**
The dance state allows each robot-builder to create their own choreographed dance written for the robot.  An example is provided in dancing.txt.

#### **Debug**
The debug state simply prints to the robot's screen an active list of the robots internal states.  This state is useful in seeing if the distance sensor is working or if the robot is connected.

#### **Explore**
In the explore state the robot will attempt to move progress forward while using its distance sensor to avoid obstacles.

#### **Race**
In the race mode the robot will race as fast as it can in a large circle while attempting to avoid obstacles using its distance sensor.

#### **Remote Control**
In this state the robot can be remotely commanded through the internet.  This requires wifi connectivity.

## Required Parts

These are the required parts if one is to use the PicoBot code as-is.  

#### **Raspberry Pi Pico W**

The wifi connectivity requires the Pico W.  This code could conceivably be modified to run on the Raspberry Pi Pico.  The robot would then lose the communication and remote-controllable functionality.

#### **CircuitPython 8**

This software was written for CircuitPython 8.  Future versions of CircuitPython may break some functionality.  For more information visit [https://circuitpython.org](https:://circuitpython.org).  

In conjunction with this we used the Adafruit CircuitPython library bundle for CircuitPython 8 in order to provide support for many of our devices.  At the time of this writing those could be found at [https://circuitpython.org/libraries](https://circuitpython.org/libraries).

#### **HC-SR04 Sonar Distance Sensor**

Please note that the default HC-SR04 sensor is 5 volts.  As such it will need special care in connecting to the Pico which is a 3V board.

#### **DRV3388 Breakout Board**

The DRV3388 is not an absolute requirement for this robot.  It is simply the device driver we used.  Any four channel H-bridge driver should work.  However, the SLOW_DECAY setting for the adafruit_motor may need to be changed.

#### **Two DC Motors**

We used two 3V to 6V DC motors with standard yellow gearboxes.  Depending on your preferences and your power supply you should be able to use a wide range of DC motors here.

#### **128 by 64 I2C SSD1306 Compatible Graphics Screen**

We used a small 128x64 3V OLED screen we found for cheap on Amazon.  There are a number of choices and suppliers.  All should work as long as they are compatible with the SSD1306 code supplied by Adafruit.




