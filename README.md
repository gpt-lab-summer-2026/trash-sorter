# Trash Sorter

Sorting your trash has never been this easy! Place a piece of trash on the platform, the Trash Sorter will analyse it through a camera, and tilts it into the correct bin.

[Demo video](https://www.youtube.com/watch?v=f7AnYyifv-E)

## Hardware

Trash Sorter is built with a raspberry pi 5, an ESP32-C6, a [spherical actuator joint](https://youtu.be/eXQK8nhIYKk?si=NN3Q2y0jIQY8u60j), a camera, and a platform system surrounded by recycling bins. Information on sorted items is shown on a QAPASS 1602A LCD screen.

## Software

The main code is in python, and it can be started automatically when the pi is turned on through a separate script. In [config.py](/config.py), the project can be set to run either headless (no monitor, default) or with a monitor. The mode with a monitor opens the camera output in a window. Change this line to True to enable monitor mode:

```
SHOW_DISPLAY = False
```

The [ESP32-C6 code](/esp32c6/esp32c6.ino) is written in C/C++ and pushed through Arduino IDE, where the motors for the joint can be manually controlled/tested. In this project, the motors are controlled through [connect_esp.py](/connect_esp.py). 
