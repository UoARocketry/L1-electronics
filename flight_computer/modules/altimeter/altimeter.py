from machine import I2C, Pin, SPI
from time import sleep
import uos
import bmp280
import sdcard

# BOARD DEFNS
I2C_SDA_PIN = 6
I2C_SCL_PIN = 7

SPI_SCK_PIN = 2
SPI_MOSI_PIN = 3
SPI_MISO_PIN = 4
SPI_CS_PIN = 5

# ALTIMETER (BMP280) INIT (I2C)
i2c = I2C(0, sda=Pin(I2C_SDA_PIN), scl=Pin(I2C_SCL_PIN), freq=400000)

# SD CARD INIT (SPI)
spi = SPI(0, baudrate=4000000, polarity=0, phase=0, sck=Pin(SPI_SCK_PIN), mosi=Pin(SPI_MOSI_PIN), miso=Pin(SPI_MISO_PIN))
cs = Pin(SPI_CS_PIN, Pin.OUT)

class Altimeter:
    def __init__(self):
        self.bmp = bmp280.BMP280(i2c)
        self.file_path = "../../../sd/altimeter_data.txt"
        self._init_sd_card()
        self._init_sd_mount()

    def _init_sd_mount(self):
        try:
            sd = sdcard.SDCard(spi, cs)
            vfs = uos.VfsFat(sd)
            uos.mount(vfs, "/sd")
            print("SD card mounted successfully.")
        except Exception as e:
            print(f"Error mounting SD card: {e}")
            raise SystemExit("Cannot proceed without SD card.")

    def _init_sd_card(self):
        try:
            with open(self.file_path, "w") as f:
                f.write("Altimeter Sensor Data\n")
                f.write("====================\n")
            print("Altimeter logging initialized.")
        except Exception as e:
            print(f"Error initializing SD card file: {e}")

    def read_data(self):
        try:
            temperature = self.bmp.temperature
            pressure = self.bmp.pressure
            return temperature, pressure
        except Exception as e:
            print(f"Error reading sensor data: {e}")
            return None, None

    def log_data(self):
        temperature, pressure = self.read_data()
        if temperature is not None and pressure is not None:
            try:
                with open(self.file_path, "a") as f:
                    f.write(f"Temperature: {temperature:.2f} °C, Pressure: {pressure:.2f} Pa\n")
            except Exception as e:
                print(f"Error writing to SD card: {e}")


# BMP280 library: https://github.com/dafvid/micropython-bmp280/tree/master 
# SD card format is FAT32
# SD card library: https://raw.githubusercontent.com/micropython/micropython-lib/master/micropython/drivers/storage/sdcard/sdcard.py