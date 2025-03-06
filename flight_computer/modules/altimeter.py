from machine import Pin, SPI
from flight_computer.libs.bmp280 import BMP280SPI
from flight_computer.modules.sdcard_manager import SDCardManager
from flight_computer.modules.error_logger import log_error

SPI_SCK_PIN = Pin(2)
SPI_TX_PIN = Pin(3)
SPI_RX_PIN = Pin(4)
SPI_CS_PIN = Pin(5, Pin.OUT, value=1)


class Altimeter:
    def __init__(
        self,
        sd_manager: SDCardManager,
        sd_file_path: str = "/sd/altimeter_data.txt",
    ):  # Functionality to initialise file path
        self.spi = SPI(0, sck=SPI_SCK_PIN, mosi=SPI_TX_PIN, miso=SPI_RX_PIN)
        self.bmp = BMP280SPI(self.spi, SPI_CS_PIN)
        self.sd_manager = sd_manager
        self.sd_file_path = sd_file_path

    def _read_data(self):
        try:
            readout = self.bmp.measurements
            temperature = readout['t']
            pressure = readout['p']
            return temperature, pressure
        except Exception as e:
            log_error(f"ERROR: Reading sensor data failed: {e}")
            return None, None

    def log_data(self):
        temperature, pressure = self._read_data()
        if temperature is not None and pressure is not None:
            altimeter_data = (
                f"Temperature: {temperature:.2f} °C, Pressure: {pressure:.2f} hPa"
            )
            self.sd_manager.log(self.sd_file_path, altimeter_data)


# BMP280 library: https://github.com/flrrth/pico-bmp280
# SD card format is FAT32
# SD card library: https://raw.githubusercontent.com/micropython/micropython-lib/master/micropython/drivers/storage/sdcard/sdcard.py
