import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from PIL import Image
import io

bucket_name = "fairyclothing"  

# Returns object name if successfully uploaded. Returns None if failed. 
def upload_file_to_s3(file_name, object_name=None):
    # If no object name is provided, use the base name of the file
    if object_name is None:
        object_name = os.path.basename(file_name)  # Use the base name of the file

    # Check if the file exists and is not empty
    if not os.path.exists(file_name):
        print(f"The file '{file_name}' was not found.")
        return None

    if os.path.getsize(file_name) == 0:
        print(f"The file '{file_name}' is empty.")
        return None

    # Create an S3 client
    s3_client = boto3.client('s3')

    # Check if the object already exists in S3
    try:
        s3_client.head_object(Bucket=bucket_name, Key=object_name)
        print(f"The object '{object_name}' already exists in S3 bucket '{bucket_name}'.")
        return None  # Object already exists, return None
    except ClientError as e:
        # If the error is 404, the object does not exist
        if e.response['Error']['Code'] == '404':
            print(f"The object '{object_name}' does not exist. Proceeding with upload.")
        else:
            print(f"An error occurred while checking for the object: {e}")
            return None

    try:
        # Upload the file to S3
        s3_client.upload_file(file_name, bucket_name, object_name)
        print(f"File '{file_name}' uploaded successfully to S3 bucket '{bucket_name}' as '{object_name}'")
        
        # Return the name under which the file was stored in S3 (the object name)
        return object_name
    except NoCredentialsError:
        print("Credentials not available.")
        return None
    except Exception as e:
        print(f"An error occurred during upload: {e}")
        return None


# Input the object name and then return the image
def download_image_from_s3(object_name):
    # Create an S3 client
    s3_client = boto3.client('s3')

    try:
        # Download the image to a byte stream
        image_data = io.BytesIO()
        s3_client.download_fileobj(bucket_name, object_name, image_data)
        image_data.seek(0)  # Move to the start of the byte stream
        
        # Open the image using PIL (Pillow)
        image = Image.open(image_data)
        
        # Display the image
        # image.show()

        return image
        
        return True
    except NoCredentialsError:
        print("Credentials not available.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

