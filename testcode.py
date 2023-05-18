from playwright.async_api import Playwright, async_playwright
import asyncio
import json


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


async def main():
    result = await get_fn_index()
    print(result)


asyncio.run(main())
