import asyncio
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

load_dotenv()

COOKIES_FILE = Path("cookies.json")


# Read login credentials from .env
def get_credentials() -> tuple[str, str]:
    return os.environ["NEXTDOOR_EMAIL"], os.environ["NEXTDOOR_PASSWORD"]


# Launch a visible Chromium browser
async def create_browser(playwright) -> Browser:
    return await playwright.chromium.launch(headless=False)


# Load saved cookies into the context; returns False if no cookie file exists
async def load_cookies(context: BrowserContext) -> bool:
    if not COOKIES_FILE.exists():
        return False
    cookies = json.loads(COOKIES_FILE.read_text())
    await context.add_cookies(cookies)
    print("Loaded cookies, skipping login.")
    return True


# Persist current session cookies to disk
async def save_cookies(context: BrowserContext) -> None:
    cookies = await context.cookies()
    COOKIES_FILE.write_text(json.dumps(cookies, indent=2))
    print("Saved cookies.")


# Fill and submit the Nextdoor login form
async def login(page: Page, email: str, password: str) -> None:
    await page.goto("https://nextdoor.com/login/?next=%2F")
    await page.fill('[data-testid="email-address-input"]', email)
    await page.fill('[data-testid="password-input"]', password)
    await page.click('[data-testid="signin_button"]')
    # Wait for redirect away from login page to confirm success
    await page.wait_for_url(lambda url: "login" not in url, timeout=15000)


# Return an authenticated context, logging in only if no cookies are saved
async def get_authenticated_context(browser: Browser) -> BrowserContext:
    context = await browser.new_context()
    if not await load_cookies(context):
        email, password = get_credentials()
        page = await context.new_page()
        await login(page, email, password)
        await save_cookies(context)
        await page.close()
    return context


async def run() -> None:
    async with async_playwright() as p:
        browser = await create_browser(p)
        context = await get_authenticated_context(browser)

        page = await context.new_page()
        await page.goto("https://nextdoor.com")

        input("Press Enter to close...")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(run())
