from machine import Pin, UART
from modules.ulora import LoRa
from modules.micropyGPS import MicropyGPS

# BOARD DEFNS
GPS_TX_PIN = 12
GPS_RX_PIN = 13

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


# MODULE CLASSES
class GPS(object):
    def __init__(self):
        # local offset: +13 for NZ timestamp
        self.gps_parser = MicropyGPS(13)
        self.gps = UART(1, 9600, tx=Pin(GPS_TX_PIN), rx=Pin(GPS_RX_PIN))

    def _set_gps_obj(self):
        """
        Reads from recv buffer and parses GPS data to a GPS object.
        Potential failures:
            - recv buffer full -> lose data; soln is to read faster
            - there are different types of GPS sentences; filtering in our end
        """
        while self.gps.any():
            # trusting the docs that it will return a string, otherwise need
            # to manually decode
            gps_data = self.gps.readline()

            # None if no new-line character or timeout
            if gps_data:
                if type(gps_data) is bytes:
                    gps_data = gps_data.decode("utf-8")

                if gps_data.startswith("$GPGGA"):
                    # available gps fields: UTC time, longtitude, latitude and altitude
                    for c in gps_data:
                        self.gps_parser.update(c)
                    break

    def get_gps_obj(self):
        self._set_gps_obj()
        return self.gps_parser


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
            # todo: log error in the SD card
            pass
