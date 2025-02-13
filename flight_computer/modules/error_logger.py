from flight_computer.modules.sdcard_manager import SDCardManager
from typing import Any

"""
Rather than a class where i have to pass an instance, all the functions are
public and global. This means that init must be explicitly called to set 
the sd_manager.

An option is to create another sd instance here but mounting is currently not thread-safe.
We can make it thread-safe but creating another instance will allocate a different lock so
its not thread-safe globally.
"""

_sd_manager: None | SDCardManager = None
_debug = None  # similar to false


def log_init(sd_manager: SDCardManager, isDebug: bool):
    _sd_manager = sd_manager
    _debug = isDebug


def log_error(error_msg: str, file_path: str = "/sd/error_log.txt"):
    if _debug:
        print(error_msg)

    if _sd_manager:
        _sd_manager.log(file_path, error_msg + "\n")
    else:
        log_debug("ERROR: error logger not initialised")


def log_debug(debug_msg: Any):
    if _debug:
        print(debug_msg)
