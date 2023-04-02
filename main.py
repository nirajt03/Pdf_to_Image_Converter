import decryption as d
import split_pdf as Sp
import pdf_to_image as PtoI
import images_with_dpi as Id
import constants as Const
import memory_cleanup as Mem_clean
import time
import os


def get_file_extension(file_path):
    get_file_name = os.path.basename(file_path)
    file_information = os.path.splitext(get_file_name)
    file_ext = file_information[1]
    print(f"File Extension: {file_ext}")

    if file_ext == Const.ENCRYPTED_EXTENSION:
        return True

    return False


def entry_point(event, context):
    start_time = time.perf_counter()

    gcp_file_path = event['name']
    print(f"Execution Start: {gcp_file_path}")

    filename = None
    if get_file_extension(gcp_file_path):
        file_path = d.__decrypt(gcp_file_path)

        file_name = Sp.__split_pdf(file_path)
    else:
        file_name = Sp.__split_pdf(gcp_file_path)

    # PDF to Image
    PtoI.__pdf_to_image(file_name)

    Mem_clean.__memory_cleanup(None, Const.FILE_EXTENSION)

    total_dpi_count = len(Const.ALL_DPI)

    for count, dpi in enumerate(Const.ALL_DPI, start=1):
        Id.__set_image_dpi(file_name, dpi)

        if count != total_dpi_count:
            Mem_clean.__memory_cleanup(dpi, None)

    print(f"Execution Complete: {gcp_file_path} :: Total Execution Time is: {round(time.perf_counter() - start_time, 2)} seconds")
