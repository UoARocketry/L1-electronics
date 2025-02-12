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
        self.sd_mounted = False # SD card status flag
        self._mount_sd()

        def _mount_sd(self):
            try:
                self.sd = sdcard.SDCard(self.spi, self.cs)
                self.vfs = uos.VfsFat(self.sd)
                uos.mount(self.vfs, "/sd") # Need to change depending on where this file will be located when finalised
                self.sd_mounted = True
                print("SD card mounted successfully.")
            except Exception as e:
                print(f"Warning: SD card mount failed: {e}")
                self.sd_mounted = False  # Mark SD unavailable

        def log(self, file_path, text):
            if not self.sd_mounted: # If SD card is not mounted, try to mount it
                print("SD card not mounted. Attempting to remount...")
                self._mount_sd()
                if not self.sd_mounted:  # If still not mounted, skip logging
                    print("SD card still not available. Skipping log.")
                    return
            
            with self.lock:  # Ensure only one thread writes at a time
                try:
                    with open(file_path, "a") as f:
                        f.write(text + "\n")
                except Exception as e:
                    print(f"Error writing to SD card: {e}")
                    self.sd_mounted = False  
                    
        def unmount_sd(self): # For unmounting SD card, although not too sure how to add this to the main.py file
            if not self.sd_mounted: # If SD card not mounted, can't unmount
                print("SD card not mounted. Nothing to unmount.")
                return

            with self.lock:  # Prevent unmounting while another thread is writing
                try:
                    uos.umount("/sd") # Need to change depending on where this file will be located when finalised
                    self.sd_mounted = False
                    print("SD card unmounted successfully.")
                except Exception as e:
                    print(f"Error unmounting SD card: {e}")
