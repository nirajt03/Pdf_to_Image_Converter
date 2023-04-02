import os

# Project Name
PROJECT_NAME = os.environ.get('PROJECT')

SOURCE_PATH = os.environ.get('SOURCE_PATH')
DESTINATION_PATH = os.environ.get('DESTINATION_PATH')

src_path = SOURCE_PATH.split('//')
SOURCE_BUCKET_NAME = src_path[1]

dest_path = DESTINATION_PATH.split('//')
DESTINATION_BUCKET_NAME = dest_path[1]

KEY = f"b{os.environ.get('KEY')}"
IV = f"b{os.environ.get('IV')}"

FILE_EXTENSION = ".pdf".lower()
ENCRYPTED_EXTENSION = ".enc".lower()

IMAGE_EXTENSION = ".png".lower()

FILE_LOCATION = "/tmp"

MAX_PDF_SIZE_IN_MB = 20
MAX_PDF_SIZE_IN_KB_POST_SPLIT = 500
MIN_PAGE_COUNT = 10
MAX_PAGE_COUNT = 30

MODE = 0o640

CONVERT_IN_MB = 1024*1024
CONVERT_IN_KB = 1024

CHUNK_SIZE = 24 * CONVERT_IN_KB

"""
    REQUIRED RESOLUTION:
    Base Resolution is 600X700
    Required Resolution is 1250*1458
    Constant base reference = 72
    So xres = 1250*72/600 -> 150
    And yres = 1458*72/700 -> 149.9657 => 150
"""
X_RES = 72
Y_RES = 72
DEFAULT_DIV = 72

DPI_1 = 300, 300
DPI_2 = 500, 500
DPI_3 = None
DPI_4 = None
DPI_5 = None

ALL_DPI = [DPI_1, DPI_2]

