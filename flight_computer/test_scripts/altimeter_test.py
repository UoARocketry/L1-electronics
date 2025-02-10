"""
Test script for the Altimeter (BMP280) module.
- verifies sensor data reading.
- checks SD card logging.
"""

from time import sleep
from modules.altimeter.altimeter import Altimeter

altimeter = Altimeter("../sd/altimeter_data.txt")
    
while True:
    temperature, pressure = altimeter.read_data()
        
    if temperature is not None and pressure is not None:
        print(f"Temperature: {temperature:.2f} °C, Pressure: {pressure:.2f} Pa")
    else:
        print("Error reading altimeter sensor data.")
        
    altimeter.log_data()
        
    sleep(0.5)