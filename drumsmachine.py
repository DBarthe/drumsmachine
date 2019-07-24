#!/usr/bin/env python3

from drumsmachine import controller
from drumsmachine import keyboard_driver
from drumsmachine import osc_driver

keyboard_driver.start()

osc_driver.start()
controller.start()  # this is blocking
