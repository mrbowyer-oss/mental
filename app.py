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
            await page.goto("https://davyhulme.intelligentgolf.co.uk/visitorbooking/", timeout=30000)

            # ✅ Updated selector
            await page.wait_for_selector(".coursestatus", timeout=10000)
            text = await page.inner_text(".coursestatus")
            await browser.close()
            return f"✅ Course Status: {text}"
    except Exception as e:
        return f"❌ Error fetching course status: {str(e)}"
