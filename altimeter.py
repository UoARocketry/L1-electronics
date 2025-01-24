from machine import I2C, Pin, SPI
from time import sleep
import uos
import bmp280
import sdcard

# BMP280 initialisation (i2c)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
bmp = BMP280(i2c)

# SD card initialisation and mounting (SPI)
spi = SPI(0, baudrate=1000000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
cs = Pin(5, Pin.OUT) 
try:
    sd = sdcard.SDCard(spi, cs)
    vfs = uos.VfsFat(sd)
    uos.mount(vfs, "/sd")
    print("SD card mounted successfully.")
except Exception as e:
    print(f"Error mounting SD card: {e}")
    raise SystemExit("Cannot proceed without SD card.")

# File path for file on SD card to be written to
file_path = "/sd/altimeter_data.txt"

# Function to log data onto the SD card
def log_data(temperature, pressure):
    try:
        with open(file_path, "a") as f:
            f.write(f"Temperature: {temperature:.2f} °C, Pressure: {pressure:.2f} Pa\n")
    except Exception as e:
        print(f"Error writing to SD card: {e}")

# Open file for writing
try:
    with open(file_path, "w") as f:
        f.write("Altimeter Sensor Data\n")
        f.write("====================\n")

    print("Logging data to: ", file_path)

    while True:
        try:
            # Read sensor data
            temperature = bmp.temperature
            pressure = bmp.pressure

            # Print data to console to verify
            print(f"Temperature: {temperature:.2f} °C, Pressure: {pressure:.2f} Pa")

            # Log data to SD card
            log_data(temperature, pressure)

        except Exception as e:
            print(f"Error reading sensor or logging data: {e}")

        # Wait before the next reading
        sleep(1)

# Stop program
except KeyboardInterrupt:
    print("Data logging stopped.")

# Unmount the SD card
finally:
    try:
        uos.umount("/sd")
        print("SD card unmounted successfully.")
    except Exception as e:
        print(f"Error unmounting SD card: {e}")

# BMP280 library: https://github.com/dafvid/micropython-bmp280/tree/master 
# SD card format is FAT32
# SD card library: https://raw.githubusercontent.com/micropython/micropython-lib/master/micropython/drivers/storage/sdcard/sdcard.py