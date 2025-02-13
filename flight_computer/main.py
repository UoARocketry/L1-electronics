from time import sleep
import _thread

from flight_computer.libs.micropyGPS import MicropyGPS
from flight_computer.modules.altimeter import Altimeter
from flight_computer.modules.sdcard_manager import SDCardManager
from flight_computer.modules.gps import GPS
from flight_computer.modules.lora import LORA
from flight_computer.modules.error_logger import log_init

# Shared SD card manager
sd_manager = SDCardManager()
log_init(sd_manager, True)


# THREAD FUNCTIONS
def radio_task():
    gps = GPS()
    lora = LORA()
    gps_file_path = "/sd/gps_data.txt"

    while True:
        gps_data: MicropyGPS = gps.get_gps_obj()
        gps_msg: str = (
            f"Time: {gps_data.timestamp}, Latitude: {gps_data.latitude}, Longitude: {gps_data.longitude}, Altitude: {gps_data.altitude}"
        )
        lora.transmit_message(gps_msg)
        sd_manager.log(gps_file_path, gps_msg)  # log msg to SD card

        sleep(0.5)


def altimeter_task():
    altimeter = Altimeter(sd_manager)
    while True:
        altimeter.log_data()
        sleep(0.5)


radio_thread = _thread.start_new_thread(radio_task, ())
# Run altimeter_task in the main thread
altimeter_task()
