from flask import Flask
import asyncio

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Flask is alive. No crash with Playwright deferred."

@app.route("/debug")
def debug():
    try:
        import shutil
        chromium_path = shutil.which("chromium") or shutil.which("chromium-browser")
        return f"Chromium path: {chromium_path or 'Not found'}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/scrape")
def scrape():
    return asyncio.run(fetch_status())

async def fetch_status():
    try:
        from playwright.async_api import async_playwright
        import shutil

        chromium_path = shutil.which("chromium") or shutil.which("chromium-browser")
        if not chromium_path:
            return "❌ Chromium not found."

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
            return f"✅ Status: {text}"
    except Exception as e:
        return f"❌ Error: {str(e)}"
