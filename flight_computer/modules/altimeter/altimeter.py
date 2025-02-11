from machine import I2C, Pin, SPI
import bmp280
from sdcard_manager import SDCardManager

I2C_SDA_PIN = 0
I2C_SCL_PIN = 1

class Altimeter: 
    def __init__(self, sd_manager, sd_file_path="../../sd/altimeter_data.txt"): # Functionality to initialise file path
        self.i2c = I2C(0, sda=Pin(I2C_SDA_PIN), scl=Pin(I2C_SCL_PIN), freq=400000)
        self.bmp = bmp280.BMP280(self.i2c)
        self.sd_manager = sd_manager
        self.sd_file_path = sd_file_path

    def _read_data(self):
        try:
            temperature = self.bmp.temperature
            pressure = self.bmp.pressure
            return temperature, pressure
        except Exception as e:
            print(f"Error reading sensor data: {e}")
            return None, None

    def log_data(self):
        temperature, pressure = self._read_data()
        if temperature is not None and pressure is not None:
            altimeter_data = f"Temperature: {temperature:.2f} °C, Pressure: {pressure:.2f} Pa"
            self.sd_manager.log(self.sd_file_path, altimeter_data)



# BMP280 library: https://github.com/dafvid/micropython-bmp280/tree/master 
# SD card format is FAT32
# SD card library: https://raw.githubusercontent.com/micropython/micropython-lib/master/micropython/drivers/storage/sdcard/sdcard.py