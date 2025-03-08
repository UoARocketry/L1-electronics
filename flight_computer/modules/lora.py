from flight_computer.libs.lora import LoRa
from machine import SPI, Pin

# from flight_computer.modules.error_logger import log_error

LORA_CHANNEL = 0
LORA_SCK = 18
LORA_MOSI = 19
LORA_MISO = 16
LORA_CS = 17
LORA_DIO0 = 20  # indicates if TX/RX done
LORA_RST = 21  # reset pin

# self defined addresses (must match with ground): : 0-254
LORA_TX_ADDR = 0
LORA_RX_ADDR = 1


class LORA(object):
    def __init__(self):
        self.spi = SPI(
            0,
            baudrate=10000000,
            sck=Pin(LORA_SCK, Pin.OUT, Pin.PULL_DOWN),
            mosi=Pin(LORA_MOSI, Pin.OUT, Pin.PULL_UP),
            miso=Pin(LORA_MISO, Pin.IN, Pin.PULL_UP),
        )
        self.lora = LoRa(
            self.spi,
            cs=Pin(LORA_CS, Pin.OUT),
        )

    def transmit_message(self, message: str):
        self.lora.send(message)
        # if not self.lora.wait_packet_sent():
        # log error in the SD card
        # log_error("ERROR: Failed to transmit from LoRa"
