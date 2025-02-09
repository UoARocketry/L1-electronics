"""
Author: long715
Test script for the NEO-6M GPS module.
- is GPS module working
- are we parsing the data correctly
- are we reading at a sufficient speed
"""

from machine import Pin, UART
from time import sleep

# additional installations: https://github.com/inmcm/micropyGPS
from modules.micropyGPS import MicropyGPS
from modules.board import *

# GPS pins:
# TX - 13 (board RX)
# RX - 12 (board TX)
# standard baud rate of neo-6m gps
gps_parser = MicropyGPS()
gps = UART(1, 9600, tx=Pin(GPS_TX_PIN), rx=Pin(GPS_RX_PIN))

while True:
    if gps.any():
        gps_data = gps.readline()  # byte string
        update_results = None
        if gps_data:
            # check due to inconsistency in docs :(
            if type(gps_data) is bytes:
                gps_data = gps_data.decode("utf-8")

            # populate gps fields
            for c in gps_data:
                update_results = gps_parser.update(c)

            # print raw data and gps obj fields
            print(gps_data)

            if update_results:
                print(gps_parser.latitude)
                print(gps_parser.longitude)
                print(gps_parser.altitude)
            else:
                print("ERROR: invalid GPS sentence")
        else:
            print("DEBUG: no GPS data received from module")

    # prevent spamming the LoRa
    sleep(0.5)
