"""
Author: long715
Test script for the radio/lora - mainly testing transmission
"""

from time import sleep

# additional installations: https://github.com/martynwheeler/u-lora
from flight_computer.libs.lora import LoRa
from flight_computer.modules.lora import *

# from flight_computer.modules.error_logger import log_debug

spi = SPI(
    0,
    baudrate=10000000,
    sck=Pin(LORA_SCK, Pin.OUT, Pin.PULL_DOWN),
    mosi=Pin(LORA_MOSI, Pin.OUT, Pin.PULL_UP),
    miso=Pin(LORA_MISO, Pin.IN, Pin.PULL_UP),
)
lora = LoRa(
    spi,
    cs=Pin(LORA_CS, Pin.OUT),
)

while True:
    # waits for prev msgs to be transmitted, if timeout, reset the buffer
    # and send new packet
    # pts of failure: some reason none of the packets gets sent
    lora.send("testing")  # w/o ack

    # explicitly wait for tx to finish cos we can only hope that
    # it did finish transmitting above, unless we test this with GS
    # if not lora.wait_packet_sent():
    #     log_debug("ERROR: timeout transmission")

    sleep(0.5)
