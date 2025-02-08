from machine import Pin, UART
from time import sleep
import _thread

from micropyGPS import MicropyGPS
from ulora import LoRa

# BOARD DEFNS
GPS_TX_PIN = 11
GPS_RX_PIN = 12

LORA_CHANNEL = 0
LORA_SCK = 24
LORA_MOSI = 25
LORA_MISO = 21
LORA_CS = 22
LORA_DIO0 = 26  # indicates if TX/RX done
LORA_RST = 27  # reset pin

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
            gps_data: str | None = self.gps.readline()

            # None if no new-line character or timeout
            if gps_data and gps_data.startswith("$GPGGA"):
                # available gps fields: UTC time, longtitude, latitude and altitude
                for c in gps_data:
                    self.gps_parser.update(c)
                break

    def get_gps_obj(self):
        self._set_gps_obj()
        return self.gps_parser


class LoRa(object):
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


# THREAD FUNCTIONS
def radio_task():
    gps = GPS()
    lora = LoRa()

    while True:
        gps_data: MicropyGPS = gps.get_gps_obj()
        gps_msg: str = (
            f"Time: {gps_data.timestamp}, Latitude: {gps_data.latitude}, Longitude: {gps_data.longitude}, Altitude: {gps_data.altitude}"
        )
        lora.transmit_message(gps_msg)
        # todo: log msg to SD card

        sleep(0.5)


radio_thread = _thread.start_new_thread(radio_task, ())
