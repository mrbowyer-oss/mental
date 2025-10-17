from shutil import which

chromium_path = which("chromium") or which("chromium-browser")
browser = await p.chromium.launch(
    headless=True,
    executable_path=chromium_path
)
