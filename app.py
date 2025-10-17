from flask import Flask, jsonify
from flask_cors import CORS
import asyncio
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "✅ Flask is alive."

@app.route("/cached")
def cached():
    try:
        with open("status.txt") as f:
            return f.read()
    except:
        return "⚠️ No cached status available."

@app.route("/scrape-and-cache")
def scrape_and_cache():
    return asyncio.run(fetch_and_cache())

async def fetch_and_cache():
    try:
        from playwright.async_api import async_playwright
        from shutil import which

        chromium_path = which("chromium") or which("chromium-browser")
        if not chromium_path:
            return "❌ Chromium not found."

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                executable_path=chromium_path
            )
            page = await browser.new_page()
            await page.goto("https://davyhulme.intelligentgolf.co.uk/visitorbooking/", timeout=30000)
            await page.wait_for_selector(".coursestatus", timeout=10000)
            text = await page.inner_text(".coursestatus")
            await browser.close()

            with open("status.txt", "w") as f:
                f.write(text)

            return f"✅ Scraped and cached: {text}"
    except Exception as e:
        return f"❌ Error: {str(e)}"
