import os
import datetime
from PIL import Image
from google.cloud import storage
import constants as Const
import get_bucket_connection as get_conn


def __set_image_dpi(filename, resolution):
    print("For RESOLUTIONS:", resolution)

    """ GCS Storage Object """
    destination_bucket = get_conn.get_bucket_connection(Const.PROJECT_NAME, Const.DESTINATION_BUCKET_NAME)

    # List of all Converted Images from PDF
    images = [list_images for list_images in os.listdir(Const.FILE_LOCATION)
              if list_images.endswith(f"_{datetime.datetime.now().strftime('%Y-%m-%d')}{Const.IMAGE_EXTENSION}") and
              os.path.isfile(os.path.join(Const.FILE_LOCATION, list_images))]

    # print("List of All IMAGES in /tmp: images)

    """
        Set DPI of the Images according to requirement 
    """
    for counter, image in enumerate(images):
        try:
            image_name_to_save = f"{filename}Page{counter + 1}{datetime.datetime.now().strftime('%Y-%m-%d')}_{resolution}{Const.IMAGE_EXTENSION}"
            image_with_resolution_location_tmp = f"{Const.FILE_LOCATION}/{image_name_to_save}"
            image_with_resolution_location_gcp = f"{filename}/{resolution}/{image_name_to_save}"

            # Location to store Image in Destination Bucket
            dest_blob_with_resolution = destination_bucket.blob(f"{image_with_resolution_location_gcp}")
            with Image.open(os.path.join(Const.FILE_LOCATION, image)) as img:
                img.save(f"{image_with_resolution_location_tmp}", dpi=resolution)
            # Save Image to Destination Bucket
            dest_blob_with_resolution.upload_from_filename(f"{image_with_resolution_location_tmp}")
        except Exception as e:
            print(f"Exception while Setting Image Resolution: {image} : {e.strerror}")

    print("5) List all Files in tmp after Setting Required Image Resolution : ", os.listdir(Const.FILE_LOCATION))
    print("Image With Resolution Complete")
    # print("Image With Resolution in /tmp: ", os.listdir(Const. FILE LOCATION))
