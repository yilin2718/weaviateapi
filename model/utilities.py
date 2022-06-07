from typing import Union
from google.cloud.storage import Client

def gcp_client():
    credentials = 'gcp_config/gcp-service-account-file.json'
    return Client.from_service_account_json(json_credentials_path=credentials)


def upload_blob(bucket_name: str, source_file_name: str, destination_blob_name: str):
    """Uploads a file to the google storage bucket.""" 
    
    storage_client = gcp_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
 
    blob.upload_from_filename(source_file_name)
 
    print(f"{source_file_name} uploaded to Storage Bucket with blob name {destination_blob_name} successfully.")


def download_blob(bucket_name: str, source_blob_name: str, destination_file_name: str):
    """Downloads a blob."""
 
    storage_client = gcp_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
 
    print(f"{source_blob_name} downloaded to file path {destination_file_name} successfully")
 
def move_blob(bucket_name: str, blob_name: str, new_blob_name: str, new_bucket_name: Union[str, None]=None):
    """
    Function for moving files between directories or buckets . it will use GCP's copy 
    function then delete the blob from the old location.
    
    inputs
    -----
    bucket_name: name of bucket
    blob_name: str, name of file 
        ex. 'data/some_location/file_name'
    new_bucket_name: name of bucket (can be same as original if we're just moving around directories)
    new_blob_name: str, name of file in new directory in target bucket 
        ex. 'data/destination/file_name'
    """
    if new_bucket_name is None:
        new_bucket_name = bucket_name

    storage_client = gcp_client()
    source_bucket = storage_client.get_bucket(bucket_name)
    source_blob = source_bucket.blob(blob_name)
    destination_bucket = storage_client.get_bucket(new_bucket_name)
 
    # copy to new destination
    new_blob = source_bucket.copy_blob(
        source_blob, destination_bucket, new_blob_name)
    # delete in old destination
    source_blob.delete()
    
    print(f'File moved from {blob_name} to {new_blob_name}')