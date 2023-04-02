import os
import fitz
import time
import datetime
from google.cloud import source
import constants as Const
import get_bucket_connection as get_conn
from PIL import Image


def __pdf_to_image(filename):
    destination_bucket = get_conn.get_bucket_connection(Const.PROJECT_NAME, Const.DESTINATION_BUCKET_NAME)

    files = [list_file for list_file in os.listdir(Const.FILE_LOCATION)
             if list_file.startswith(f"{filename}Page") and
             os.path.isfile(os.path.join(Const.FILE_LOCATION, list_file))]

    for counter, file_list in enumerate(files):
        try:
            if file_list:
                image_name = f"{filename}Page{counter + 1}_{datetime.datetime.now().strftime('%Y-%m-%d')}{Const.IMAGE_EXTENSION}"

                dest_blob = destination_bucket.blob(f"{filename}/Original/{image_name}")

                pdf = fitz.open(f"{Const.FILE_LOCATION}/{filename}Page{counter + 1}{Const.FILE_EXTENSION}",
                                filetype=f"{Const.FILE_EXTENSION}")
                page = pdf.loadPage(0)

                mat = fitz.Matrix(Const.X_RES / Const.DEFAULT_DIV, Const.Y_RES / Const.DEFAULT_DIV)
                pix = page.getPixmap(matrix=mat)

                image_location = f"{Const.FILE_LOCATION}/{image_name}"
                pix.writeImage(f"{image_location}")

                dest_blob.upload_from_filename(f"{image_location}")

            else:
                print(f"{file_list} doesnt exist")
        except Exception as e:
            print(f"Exception while PDF to Image Conversion: {e}")

    print("4) List of Original Resolution of Images in tmp: ", os.listdir(Const.FILE_LOCATION))
    print("PDF to Image Complete")
