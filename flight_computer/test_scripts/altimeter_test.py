"""
Test script for the Altimeter (BMP280) module.
- Verifies sensor data reading.
- Checks SD card logging functionality.
"""

from time import sleep
from modules.altimeter.altimeter import Altimeter

altimeter = Altimeter()
    
while True:
    temperature, pressure = altimeter.read_data()
        
    if temperature is not None and pressure is not None:
        print(f"Temperature: {temperature:.2f} °C, Pressure: {pressure:.2f} Pa")
    else:
        print("Error reading altimeter sensor data.")
        
    altimeter.log_data()
        
    sleep(0.5)