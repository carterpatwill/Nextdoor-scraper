import asyncio
from playwright.async_api import async_playwright


async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://nextdoor.com")
        await page.click('[data-testid="header-log-in"]')
        input("Press Enter to close...")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(run())
