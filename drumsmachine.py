#!/usr/bin/env python3

from drumsmachine import controller
from drumsmachine import keyboard_driver

keyboard_driver.start()

controller.start()  # this is blocking
