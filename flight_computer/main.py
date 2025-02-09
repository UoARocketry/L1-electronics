from time import sleep
import _thread

from modules.micropyGPS import MicropyGPS
from modules.board import *


# THREAD FUNCTIONS
def radio_task():
    gps = GPS()
    lora = LORA()

    while True:
        gps_data: MicropyGPS = gps.get_gps_obj()
        gps_msg: str = (
            f"Time: {gps_data.timestamp}, Latitude: {gps_data.latitude}, Longitude: {gps_data.longitude}, Altitude: {gps_data.altitude}"
        )
        lora.transmit_message(gps_msg)
        # todo: log msg to SD card

        sleep(0.5)


radio_thread = _thread.start_new_thread(radio_task, ())
