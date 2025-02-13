"""
Author: long715
Test script for the radio/lora - mainly testing transmission
"""

from time import sleep

# additional installations: https://github.com/martynwheeler/u-lora
from flight_computer.libs.ulora import LoRa
from flight_computer.modules.lora import *
from flight_computer.modules.error_logger import log_debug

lora = LoRa(
    (LORA_CHANNEL, LORA_SCK, LORA_MOSI, LORA_MISO),
    LORA_DIO0,
    LORA_TX_ADDR,
    LORA_CS,
    LORA_RST,
)

while True:
    # waits for prev msgs to be transmitted, if timeout, reset the buffer
    # and send new packet
    # pts of failure: some reason none of the packets gets sent
    lora.send("testing", LORA_RX_ADDR)  # w/o ack

    # explicitly wait for tx to finish cos we can only hope that
    # it did finish transmitting above, unless we test this with GS
    if not lora.wait_packet_sent():
        log_debug("ERROR: timeout transmission")

    sleep(0.5)
