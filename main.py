#!/usr/bin/env python3

import time
from src.temperature import TemperatureModule

try:
    print('Starting sensors')
    temperature = TemperatureModule(3, 600)
    while True:
        time.sleep(5)

except KeyboardInterrupt:
    print('Exiting due to keyboard interrupt')

finally:
    print('Sensor script ended')
