import runpod
import subprocess
import requests
import time
from typing import List
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, generate_blob_sas, AccountSasPermissions, ResourceTypes
from azure.core.exceptions import ResourceExistsError
from datetime import datetime, timedelta
from io import BytesIO
import os
import base64
import io

CONNECTION_STRING =  os.environ.get('CONNECTION_STRING')
ACCOUNT_NAME = os.environ.get('ACCOUNT_NAME')
ACCOUNT_KEY = os.environ.get('ACCOUNT_KEY')
CONTAINER_NAME = os.environ.get('CONTAINER_NAME')


def check_api_availability(host):
    while True:
        try:
            response = requests.get(host)
            return
        except requests.exceptions.RequestException as e:
            print(f"API is not available, retrying in 200ms... ({e})")
        except Exception as e:
            print('something went wrong')
        time.sleep(200/1000)

check_api_availability("http://127.0.0.1:7860/sdapi/v1/img2img")

print('run handler')

def handler(event):
    '''
    This is the handler function that will be called by the serverless.
    '''
    print('got event')
    #print(event)

    fileName=event["input"]["filename"]

    
    try:
        response = requests.post(url=f'http://127.0.0.1:7860/sdapi/v1/img2img', json=event["input"])

        json = response.json()
    # do the things

        print(json)
    except Exception:
        return {"error":json}
    # return the output that you want to be returned like pre-signed URLs to output artifacts
    # upload_image_to_container(json["output"]["images"][0],fileName)
    base64_image=json["images"][0]
    blob_service_client = BlobServiceClient.from_connection_string(
        CONNECTION_STRING)

    try:
            container_client = blob_service_client.create_container(
            CONTAINER_NAME, public_access=None)
            print(
            f"Container '{CONTAINER_NAME}' created successfully with private access.")
    except ResourceExistsError:
        container_client = blob_service_client.get_container_client(
            CONTAINER_NAME)
        container_client.set_container_access_policy(
            signed_identifiers={}, public_access=None)
        print(
            f"Container '{CONTAINER_NAME}' already exists and is now set to private access.")
        blob_client = container_client.get_blob_client(fileName)

        image_bytes = base64.b64decode(base64_image)
        image_obj = io.BytesIO(image_bytes)

        image_obj.seek(0)  # Ensure the file object is at the beginning
        blob_client.upload_blob(image_obj, overwrite=True)
        print(f"Image '{fileName}' uploaded to container '{container_client.container_name}'.")
        image_obj.seek(0)
        
    return json

runpod.serverless.start({"handler": handler})


