from flight_computer.libs.ulora import LoRa
from flight_computer.modules.error_logger import log_error

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
        self.lora = LoRa(
            (LORA_CHANNEL, LORA_SCK, LORA_MOSI, LORA_MISO),
            LORA_DIO0,
            LORA_TX_ADDR,
            LORA_CS,
            LORA_RST,
        )

    def transmit_message(self, message: str):
        self.lora.send(message, LORA_RX_ADDR)
        if not self.lora.wait_packet_sent():
            # log error in the SD card
            log_error("ERROR: Failed to transmit from LoRa")
