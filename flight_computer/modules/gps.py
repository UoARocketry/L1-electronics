from machine import Pin, UART
from flight_computer.libs.micropyGPS import MicropyGPS
from flight_computer.modules.error_logger import log_error

# BOARD DEFNS
GPS_TX_PIN = 12
GPS_RX_PIN = 13


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
            - endless loop
        """
        while self.gps.any():
            gps_data = self.gps.readline()

            # None if no new-line character or timeout
            if gps_data:
                if type(gps_data) is bytes:
                    gps_data = gps_data.decode("utf-8")

                if gps_data.startswith("$GPGGA"):
                    update_status = False
                    # available gps fields: UTC time, longtitude, latitude and altitude
                    for c in gps_data:
                        update_status = self.gps_parser.update(c)

                    if not update_status:
                        log_error("ERROR: Invalid GPS sentence")
                    else:
                        break

    def get_gps_obj(self):
        self._set_gps_obj()
        return self.gps_parser
