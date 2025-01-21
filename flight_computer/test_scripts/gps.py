"""
Author: long715
Test script for the NEO-6M GPS module.
"""

from machine import Pin, UART
from time import sleep

# additional installations: https://github.com/inmcm/micropyGPS
from micropyGPS import MicropyGPS

# GPS pins:
# TX - 12 (board RX)
# RX - 11 (board TX)
# standard baud rate of neo-6m gps
gps_parser = MicropyGPS()
gps = UART(1, 9600, tx=Pin(11), rx=Pin(12))

while True:
    if gps.any():
        gps_data = gps.readline()
        if gps_data:
            # populate gps fields
            for c in gps_data:
                gps_parser.update(c)

        # print raw data and gps obj fields
        print(gps_data)
        print(gps_parser.latitude)
        print(gps_parser.longitude)
        print(gps_parser.altitude)

    sleep(0.5)
