from flight_computer.modules.sdcard_manager import SDCardManager

"""
Rather than a class where i have to pass an instance, all the functions are
public and global. This means that init must be explicitly called to set 
the sd_manager.

An option is to create another sd instance here but mounting is currently not thread-safe.
We can make it thread-safe but creating another instance will allocate a different lock so
its not thread-safe globally.
"""

_sd_manager: None | SDCardManager = None
_DEBUG = True  # set to False if flight


def log_init(sd_manager: SDCardManager):
    _sd_manager = sd_manager


def log_error(error_msg: str, file_path: str = "/sd/error_log.txt"):
    if _DEBUG:
        print(error_msg)

    if _sd_manager:
        _sd_manager.log(file_path, error_msg + "\n")
    else:
        print("ERROR: error logger not initialised")
