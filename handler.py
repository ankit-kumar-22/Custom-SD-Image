import runpod
import requests
import time
from azure.storage.blob import BlobServiceClient
from io import BytesIO
import os
import base64
import io
import json
from playwright.sync_api import Playwright, sync_playwright


CONNECTION_STRING = os.environ.get('CONNECTION_STRING')
ACCOUNT_NAME = os.environ.get('ACCOUNT_NAME')
ACCOUNT_KEY = os.environ.get('ACCOUNT_KEY')
CONTAINER_NAME = os.environ.get('CONTAINER_NAME')


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


check_api_availability("http://127.0.0.1:3000/run/predict/")

print('run handler')


def handler(event):
    '''
    This is the handler function that will be called by the serverless.
    '''
    print('got event')
    # print(event)

    def get_fn_index():
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=True, args=["--start-maximized"])
            context = browser.new_context(no_viewport=True)
            page = context.new_page()
            page.goto("http://127.0.0.1:3000/")
            page.get_by_role("button", name="img2img", exact=True).click()
            page.get_by_role("button", name="Inpaint upload").click()
            page.wait_for_timeout(1000)
            with page.expect_request("**/predict") as request:
                page.get_by_role("button", name="Generate").click()
            post_data_json = json.loads(request.value.post_data)
            fn_index = post_data_json['fn_index']
            context.close()
            browser.close()
        return fn_index

    def save_data(response_to_save):

        blob_service_client = BlobServiceClient.from_connection_string(
            CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(
            CONTAINER_NAME)
        print(
            f"Container '{CONTAINER_NAME}' created successfully with private access.")
        blob_client = container_client.get_blob_client(fileName)
        json_str = json.dumps(response_to_save)
        file_obj = BytesIO(json_str.encode())

        file_obj.seek(0)  # Ensure the file object is at the beginning
        blob_client.upload_blob(file_obj, overwrite=True)
        print(
            f"File '{fileName}' uploaded to container '{container_client.container_name}'.")
        file_obj.seek(0)

    fileName = event["input"]["filename"]
    fn_index_flag = event["input"]["fn_index"]

    if (fn_index_flag == True):
        fn_index = get_fn_index()
        return {"refresh_worker": True, "fn_index": fn_index}
    else:
        try:
            response = requests.post(
                url=f'http://127.0.0.1:3000/run/predict/', json=event["input"])

            json_response = response.json()
            save_data(json_response)
        except Exception:
            return {"error": json_response}

    return {"refresh_worker": True, "data": json_response}


runpod.serverless.start({"handler": handler})
