"""
Test script for the Altimeter (BMP280) module.
- verifies sensor data reading.
- checks SD card logging.
"""

from time import sleep
from flight_computer.modules.altimeter import Altimeter
from flight_computer.modules.sdcard_manager import SDCardManager
from flight_computer.modules.error_logger import log_debug

sd_manager = SDCardManager()
altimeter = Altimeter(sd_manager)

while True:
    temperature, pressure = altimeter._read_data()

    if temperature is not None and pressure is not None:
        log_debug(f"Temperature: {temperature:.2f} °C, Pressure: {pressure:.2f} Pa")
    else:
        log_debug("Error reading altimeter sensor data.")

    altimeter_data = f"Temperature: {temperature:.2f} °C, Pressure: {pressure:.2f} Pa"
    altimeter.sd_manager.log("../sd/altimeter_data.txt", altimeter_data)

    sleep(0.5)
