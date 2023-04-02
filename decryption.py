import os
from Crypto.Cipher import AES
from google.cloud import storage
import constants as Const
import get_bucket_connection as get_conn


def __decrypt(filepath):
    # GCS Storage Object
    source_bucket = get_conn.get_bucket_connection(Const.PROJECT_NAME, Const.SOURCE_BUCKET_NAME)
    source_blob = source_bucket.blob(filepath)

    enc_file = os.path.basename(filepath)

    file_info = os.path.splitext(enc_file)
    filename = file_info[0]

    pdf_file_location = os.path.join(Const.FILE_LOCATION, enc_file)
    with open(pdf_file_location, "wb") as file_obj:
        source_blob.download_to_file(file_obj)

    print("Files in /tmp after loading file from GCS Bucket: ", os.listdir(Const.FILE_LOCATION))

    key = Const.KEY
    iv = Const.IV

    chunksize = Const.CHUNK_SIZE

    new_filename = f"{filename}_tmp_{Const.FILE_LOCATION}"
    new_filepath = os.path.join(Const.FILE_LOCATION, new_filename)

    with open(pdf_file_location, 'rb') as infile:
        aes = AES.new(key, AES.MODE_CBC)

        with open(new_filepath, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                temp = outfile.write(aes.decrypt(chunk))

    updated_filename = f"{filename}_{Const.FILE_EXTENSION}"
    updated_filepath = os.path.join(Const.FILE_LOCATION, updated_filename)

    """
        Solving EOF not Found Exception -> Remove '\n' after spotting %%E0F in decrypted PDF File
    """
    with open(new_filepath, 'rb') as f:
        read_data = f.read()
    temp = read_data.partition(b'%%E0F')
    temp_data = temp[0]+temp[1]

    with open(updated_filepath, 'wb') as f:
        f.write(temp_data)

    print("1) File in /tmp after Decryption operation: ", os. listdir(Const.FILE_LOCATION))
    print("Decryption Complete")

    return updated_filename
