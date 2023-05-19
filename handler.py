import base64
import runpod
import requests
import time
from azure.storage.blob import BlobServiceClient
import os


CONNECTION_STRING = os.environ.get('CONNECTION_STRING')
ACCOUNT_NAME = os.environ.get('ACCOUNT_NAME')
ACCOUNT_KEY = os.environ.get('ACCOUNT_KEY')
CONTAINER_NAME = os.environ.get('CONTAINER_NAME')
BASE_URI = "http://127.0.0.1"
PORT_NO = "3000"
HEALTHCHECK_API_ENPOINT = "/sdapi/v1/options"
IMG2IMG_API_ENPOINT = "/sdapi/v1/img2img"


def check_api_availability(host):
    while True:
        try:
            response = requests.get(host)
            return
        except requests.exceptions.RequestException as e:
            print(f"API is not available, retrying in 4s... ({e})")
        except Exception as e:
            print('something went wrong')
        time.sleep(4)


time.sleep(3)
check_api_availability(f"{BASE_URI}:{PORT_NO}{HEALTHCHECK_API_ENPOINT}")

print('run handler')


def handler(event):
    '''
    This is the handler function that will be called by the serverless.
    '''
    print('got event')
    username = event["input"]["username"]

    try:
        response = requests.post(
            url=f"{BASE_URI}:{PORT_NO}{IMG2IMG_API_ENPOINT}", json=event["input"])

        json_response = response.json()

        # Create a blob service client
        blob_service_client = BlobServiceClient.from_connection_string(
            CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(
            CONTAINER_NAME)

        print(
            f"Container '{CONTAINER_NAME}' created successfully with private access.")

        # Extract images from the API response
        print(json_response)
        images = json_response["images"]

        # Decode each image and upload it to Azure Blob Storage
        for index, image in enumerate(images, start=1):
            # Decode the base64 image
            img_data = base64.b64decode(image)

            # Generate blob name
            blob_name = f"SD_{username}_{index}.png"

            # Get blob client
            blob_client = container_client.get_blob_client(blob_name)

            # Upload the image data to Azure Blob Storage
            blob_client.upload_blob(img_data, overwrite=True)

            print(
                f"Image '{blob_name}' uploaded to container '{container_client.container_name}'.")

    except Exception as e:
        print(f"Exception: {e}")
        return {"refresh_worker": True, "success": False, "message": json_response}

    return {"refresh_worker": True, "success": True, "message": "image generated sucessfully"}


runpod.serverless.start({"handler": handler})
