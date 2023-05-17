from playwright.sync_api import sync_playwright, Error
import json


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
        with page.expect_request("**/predict/") as request:
            page.get_by_role("button", name="Generate").click()
        post_data_json = json.loads(request.value.post_data)
        fn_index = post_data_json['fn_index']
        context.close()
        browser.close()
    return fn_index


print(get_fn_index())
