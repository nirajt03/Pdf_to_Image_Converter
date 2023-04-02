from google.cloud import storage


def get_bucket_connection(project_name, bucket_name):
    try:
        gcs_client = storage.Client(project=project_name)
        bucket = gcs_client.get_bucket(bucket_name)

        return bucket

    except Exception as e:
        print(f"Exception While Creating Bucket Object: {e}")

    return None
