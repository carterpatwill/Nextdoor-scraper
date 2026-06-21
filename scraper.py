import asyncio
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()


async def run():
    email = os.environ.get("NEXTDOOR_EMAIL", "")
    password = os.environ.get("NEXTDOOR_PASSWORD", "")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://nextdoor.com/login/?next=%2F")

        await page.fill('[data-testid="email-address-input"]', email)
        await page.fill('[data-testid="password-input"]', password)
        await page.click('[data-testid="signin_button"]')

        input("Press Enter to close...")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(run())
