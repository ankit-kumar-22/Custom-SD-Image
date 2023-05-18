import runpod
import requests
import time
from azure.storage.blob import BlobServiceClient
from io import BytesIO
import os
import base64
import io
from playwright.async_api import Playwright, async_playwright
import asyncio
import json


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


check_api_availability("http://127.0.0.1:3000/sdapi/v1/options")

print('run handler')


def handler(event):
    '''
    This is the handler function that will be called by the serverless.
    '''
    print('got event')
    # print(event)

    async def get_fn_index():
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=True, args=["--start-maximized"])
            context = await browser.new_context(no_viewport=True)
            page = await context.new_page()
            await page.goto("http://127.0.0.1:3000/")
            await page.get_by_role("button", name="img2img", exact=True).click()
            await page.get_by_role("button", name="Inpaint upload").click()
            await asyncio.sleep(1)
            async with page.expect_request("**/predict/") as request_info:
                await page.get_by_role("button", name="Generate").click()
            request = await request_info.value
            request_body_json = json.loads(request.post_data)
            fn_index = request_body_json['fn_index']
            await context.close()
            await browser.close()
        return fn_index

    def save_data(response_to_save, file_name):

        blob_service_client = BlobServiceClient.from_connection_string(
            CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(
            CONTAINER_NAME)
        print(
            f"Container '{CONTAINER_NAME}' created successfully with private access.")
        blob_client = container_client.get_blob_client(file_name)
        json_str = json.dumps(response_to_save)
        file_obj = BytesIO(json_str.encode())

        file_obj.seek(0)  # Ensure the file object is at the beginning
        blob_client.upload_blob(file_obj, overwrite=True)
        print(
            f"File '{file_name}' uploaded to container '{container_client.container_name}'.")
        file_obj.seek(0)

    fn_index_flag = event["input"]["fn_index"]

    if (fn_index_flag == True):
        print('TESTING')
        fn_index = get_fn_index()
        return {"refresh_worker": True, "fn_index": fn_index}
    else:
        try:
            response = requests.post(
                url=f'http://127.0.0.1:3000/run/predict/', json=event["input"])

            json_response = response.json()
            fileName = event["input"]["filename"]
            save_data(json_response, fileName)
        except Exception:
            return {"error": json_response}

    return {"refresh_worker": True, "data": json_response}


runpod.serverless.start({"handler": handler})
