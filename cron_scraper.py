import asyncio
from playwright.async_api import async_playwright
from shutil import which

async def run():
    chromium_path = which("chromium") or which("chromium-browser")
    if not chromium_path:
        print("❌ Chromium not found.")
        return

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

        # Save to file or print to logs
        with open("status.txt", "w") as f:
            f.write(text)
        print("✅ Scraped and saved:", text)

asyncio.run(run())
