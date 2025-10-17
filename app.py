from flask import Flask
import asyncio
from playwright.async_api import async_playwright
from shutil import which

app = Flask(__name__)

@app.route("/")
def course_status():
    return asyncio.run(fetch_status())

@app.route("/debug")
def debug():
    path = which("chromium") or which("chromium-browser")
    return f"Detected Chromium binary: {path or 'Not found'}"

async def fetch_status():
    try:
        chromium_path = which("chromium") or which("chromium-browser")
        if not chromium_path:
            return "Chromium not found on system."

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                executable_path=chromium_path
            )
            page = await browser.new_page()
            await page.goto("https://davyhulme.intelligentgolf.co.uk/visitorbooking/", timeout=20000)
            await page.wait_for_selector(".igcourse_status_text", timeout=10000)
            text = await page.inner_text(".igcourse_status_text")
            await browser.close()
            return text
    except Exception as e:
        return f"Error fetching course status: {str(e)}"
