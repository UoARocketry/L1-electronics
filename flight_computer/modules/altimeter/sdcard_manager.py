from machine import SPI, Pin
import uos
import sdcard
import _thread

# Changed to SPI1 GPIO 8-11
SPI_SCK_PIN   = 8
SPI_MOSI_PIN  = 9
SPI_MISO_PIN  = 10
SPI_CS_PIN    = 11

class SDCardManager:
    def __init__(self):
        self.spi = SPI(1, baudrate=4000000, polarity=0, phase=0, sck=Pin(SPI_SCK_PIN), mosi=Pin(SPI_MOSI_PIN), miso=Pin(SPI_MISO_PIN))
        self.cs = Pin(SPI_CS_PIN, Pin.OUT)
        self.lock = _thread.allocate_lock()  # Lock for thread safety
        self._mount_sd()

    def _mount_sd(self):
        try:
            self.sd = sdcard.SDCard(self.spi, self.cs)
            self.vfs = uos.VfsFat(self.sd)
            uos.mount(self.vfs, "/sd") # Need to change depending on where this file will be located when finalised
            print("SD card mounted successfully.")
        except Exception as e:
            print(f"Error mounting SD card: {e}")
            raise SystemExit("Error mounting without SD card.")

    def log(self, file_path, text):
        with self.lock:  # Ensure only one thread writes at a time
            try:
                with open(file_path, "a") as f:
                    f.write(text + "\n")
            except Exception as e:
                print(f"Error writing to SD card: {e}")

    def unmount_sd(self): # For unmounting SD card, although not too sure how to add this to the main.py file
        with self.lock:  # Prevent unmounting while another thread is writing
            try:
                uos.umount("/sd") # Need to change depending on where this file will be located when finalised
                print("SD card unmounted successfully.")
            except Exception as e:
                print(f"Error unmounting SD card: {e}")

