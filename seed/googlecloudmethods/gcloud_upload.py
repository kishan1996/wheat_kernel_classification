from google.cloud import storage


def upload_cloud( source_file_name, destination_blob_name=None):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket('ineuroninternship.appspot.com')
    blob = bucket.blob(source_file_name.filename)

    #blob.upload_from_filename(source_file_name)
    blob.upload_from_string(source_file_name.read(), content_type=source_file_name.content_type)

    # print(
    #     "File {} uploaded to {}.".format(
    #         source_file_name, destination_blob_name
    #     )
    # )
