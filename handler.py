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
import json

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

check_api_availability("http://127.0.0.1:3000/sdapi/v1/img2img")

print('run handler')

def handler(event):
    '''
    This is the handler function that will be called by the serverless.
    '''
    print('got event')
    #print(event)

    fileName=event["input"]["filename"]

    
    try:
        response = requests.post(url=f'http://127.0.0.1:3000/sdapi/v1/img2img', json=event["input"])

        json_response = response.json()
    # do the things

        print(json_response)
    except Exception:
        return {"error":json_response}
    blob_service_client = BlobServiceClient.from_connection_string(
        CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(
            CONTAINER_NAME)
    print(
            f"Container '{CONTAINER_NAME}' created successfully with private access.")
    blob_client = container_client.get_blob_client(fileName)

        # Convert the JSON data to a string
    json_str = json.dumps(json_response)

        # Convert the string to BytesIO object
    file_obj = BytesIO(json_str.encode())

    file_obj.seek(0)  # Ensure the file object is at the beginning
    blob_client.upload_blob(file_obj, overwrite=True)
    print(
        f"File '{fileName}' uploaded to container '{container_client.container_name}'.")

    file_obj.seek(0)
        
    return {"refresh_worker": True, "job_results": json_response}

runpod.serverless.start({"handler": handler})


