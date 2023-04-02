import os
import sys
import shutil
from PyPDF2 import PdfFileReader, PdfFileWriter, utils
from google.cloud import storage
import constants as Const
import get_bucket_connection as get_conn


def __split_pdf(pdf_file_path):
    file_with_extension = os.path.basename(pdf_file_path)

    print("PDF File Path: ", pdf_file_path)
    print(f"Base: {file_with_extension}")

    file_info = os.path.splitext(file_with_extension)
    filename = file_info[0]

    print(f"FileName: {filename}")

    pdf_file_location = os.path.join(Const.FILE_LOCATION, file_with_extension)

    if not os.path.exists(pdf_file_path):
        source_bucket = get_conn.get_bucket_connection(Const.PROJECT_NAME, Const.SOURCE_BUCKET_NAME)
        source_blob = source_bucket.blob(pdf_file_path)

        with open(pdf_file_location, "wb") as file_obj:
            source_blob.download_to_file(file_obj)

    pdf_file_size = round(os.stat(f"{pdf_file_location}").st_size / Const.CONVERT_IN_MB, 2)
    print("PDF File Size in MB: ", pdf_file_size)

    if pdf_file_size > Const.MAX_PDF_SIZE_IN_MB:
        print(f"PDF File Size exceeded {Const.MAX_PDF_SIZE_IN_MB}MB")

    pdf = None
    try:
        pdf = PdfFileReader(open(pdf_file_location, "rb"))
    except OSError as osError:
        print(f"Unable to open/read file: {osError}")
    except utils.PdfReadError as invalid_file:
        print(f"Invalid PDF File: {invalid_file}")
    else:
        pass

    page_count = pdf.getNumPages()
    print(f"Total Pae Count: {page_count}")

    if page_count < Const.MIN_PAGE_COUNT or page_count > Const.MAX_PAGE_COUNT:
        print(f"Page Count ie., {page_count} Pages, is not satisfying the given range [10-30]")

    for page_num in range(page_count):
        splitted_pdf = f"{filename}Page{page_num + 1}{Const.FILE_EXTENSION}"
        try:
            pdfWriter = PdfFileWriter()
            pdfWriter.addPage(pdf.getPage(page_num))
            single_pg_pdf_file_path = os.path.join(Const.FILE_LOCATION, splitted_pdf)

            with open(single_pg_pdf_file_path, "wb") as file_obj:
                pdfWriter.write(file_obj)

            single_pg_pdf_file_size = round(os.stat(single_pg_pdf_file_path).st_size / Const.CONVERT_IN_KB, 2)

            if single_pg_pdf_file_size > Const.MAX_PDF_SIZE_IN_KB_POST_SPLIT:
                print(f"{splitted_pdf} size from PDF file exceeded {Const.MAX_PDF_SIZE_IN_KB_POST_SPLIT}KB")

        except Exception as e:
            print(f"Exception while splitting PDF: {e}")

    print("3) List Files in tmp after splitting: ", os.listdir(Const.FILE_LOCATION))
    print("PDF Splitting Complete")
    return filename
