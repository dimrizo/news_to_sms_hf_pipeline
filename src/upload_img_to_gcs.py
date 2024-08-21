from google.cloud import storage
import datetime

def upload_blob(bucket_name, source_file_name, destination_blob_base_name):
    """Uploads a file to the G bucket."""

    # Generate a timestamp & insert to file name
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    destination_blob_name = f"{destination_blob_base_name}-{timestamp}.png"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    # Make the blob publicly viewable
    blob.make_public()

    print(f"File {source_file_name} uploaded to {destination_blob_name} and made public.")
    print(f"Public URL: {blob.public_url}")

    return blob.public_url

if __name__ == '__main__':
    # Google Bucket parameters
    bucket_name = 'sm_auto_first'
    source_file_name = 'io_files/output_image_astro.png'
    destination_blob_base_name = 'uploads/story'  # optional parameter to customize the destination path and file name in the bucket

    upload_blob(bucket_name, source_file_name, destination_blob_base_name)
