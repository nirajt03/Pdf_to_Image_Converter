import os
import glob
from pathlib import Path
import constants as Const

"""
    Perform Memory Cleanup of unnecessary files as memory is limited for function execution [Currently 256MB]
    Max provided by GCP us upto 8Gb as of 7/5/2021
"""


def __memory_cleanup(resolution, extension):
    if extension:
        for del_file in Path(Const.FILE_LOCATION).glob(f"*{extension}"):
            try:
                del_file.unlink()
            except OSError as e:
                print(f"ERROR while deleting File: {del_file} : {e.strerror}")

    if resolution:
        for del_image in Path(Const.FILE_LOCATION).glob(f"*_{resolution}{Const.IMAGE_EXTENSION}"):
            try:
                del_image.unlink()
            except OSError as e:
                print(f"ERROR while deleting Image: {del_image} : {e.strerror}")

    print("6) List all Files in tmp after memory Cleanup: ", os.listdir(Const.FILE_LOCATION))
    print("Memory Cleanup Successful")
