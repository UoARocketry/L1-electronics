from machine import SPI, Pin
import uos
import sdcard


# Changed to SPI1 GPIO 8-11
SPI_SCK_PIN   = 8
SPI_MOSI_PIN  = 9
SPI_MISO_PIN  = 10
SPI_CS_PIN    = 11

# Separate class for managing SD card
class SDCardManager:
    def __init__(self, file_path): # Functionality to initialise file path
        self.spi = SPI(1, baudrate=4000000, polarity=0, phase=0, sck=Pin(SPI_SCK_PIN), mosi=Pin(SPI_MOSI_PIN), miso=Pin(SPI_MISO_PIN))
        self.cs = Pin(SPI_CS_PIN, Pin.OUT)
        self.file_path = file_path
        self.mount_sd()
        self.init_file()

    def mount_sd(self):
        try:
            sd = sdcard.SDCard(self.spi, self.cs)
            vfs = uos.VfsFat(sd)
            uos.mount(vfs, "/sd") # Need to change depending on where this file will be located when finalised
            print("SD card mounted successfully.")
        except Exception as e:
            print(f"Error mounting SD card: {e}")
            raise SystemExit("Error mounting without SD card.")

    def init_file(self):
        try:
            with open(self.file_path, "w") as f:
                f.write("Data Logging Started\n")
                f.write("====================\n")
            print("SD logging initialised at:", self.file_path)
        except Exception as e:
            print(f"Error initialising SD card file: {e}")

    def log(self, text):
        try:
            with open(self.file_path, "a") as f:
                f.write(text + "\n")
        except Exception as e:
            print(f"Error writing to SD card: {e}")

    def unmount_sd(self): # For unmounting SD card, although not too sure how to add this to the main.py file
        try:
            uos.umount("/sd") # Need to change depending on where this file will be located when finalised
            print("SD card unmounted successfully.")
        except Exception as e:
            print(f"Error unmounting SD card: {e}")
