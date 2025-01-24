"""
Author: long715
Test script for the radio/lora - mainly testing transmission
"""

# additional installations: https://github.com/martynwheeler/u-lora
from ulora import LoRa
from time import sleep

# (channel, sck, mosi, miso)
spi_pins = (0, 24, 25, 21)
cs_pin = 22
dio0_pin = 26
rst_pin = 27
tx_addr = 0  # 0-254
rx_addr = 1

lora = LoRa(spi_pins, dio0_pin, tx_addr, cs_pin, rst_pin)

while True:
    # waits for prev msgs to be transmitted, if timeout, reset the buffer
    # and send new packet
    # pts of failure: some reason none of the packets gets sent
    lora.send("testing", rx_addr)  # w/o ack

    # explicitly wait for tx to finish cos we can only hope that
    # it did finish transmitting above, unless we test this with GS
    if not lora.wait_packet_sent():
        print("ERROR: timeout transmission")

    sleep(0.5)
