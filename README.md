# Nextdoor Marketplace Scraper

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-1.60-2EAD33?logo=playwright&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

A Python script that uses **Playwright** browser automation to scrape listings from [Nextdoor](https://nextdoor.com)'s Marketplace. Supports cookie-based session persistence (log in once, reuse the session indefinitely), distance filtering, and a free-items-only mode.

---

## Features

- **Persistent login** — saves session cookies on first run; subsequent runs skip the login step entirely
- **Distance filter** — restrict results to 1, 3, 5, 7, 10, 15, 20, 30, 40, or 50 miles
- **Free items toggle** — optionally show only free listings
- **Clean structured output** — each listing returns `price`, `title`, `time_posted`, `distance`, and `neighborhood`

---

## Tech Stack

| Tool | Purpose |
|---|---|
| [Playwright](https://playwright.dev/python/) | Browser automation & DOM scraping |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | Credential management via `.env` |

---

## Prerequisites

- Python 3.10+
- pip

---

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/carterpatwill/Nextdoor-scraper.git
cd Nextdoor-scraper

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install the Chromium browser required by Playwright
playwright install chromium
```

---

## Configuration

Copy `.env.example` to `.env` and fill in your Nextdoor credentials:

```bash
cp .env.example .env
```

```env
NEXTDOOR_EMAIL=your_email@example.com
NEXTDOOR_PASSWORD=your_password
```

> **Note:** Credentials are only used to authenticate against Nextdoor and are never sent elsewhere. The `.env` file is git-ignored.

---

## Usage

Adjust the parameters in the `run()` call at the bottom of `scraper.py`, then execute the script:

```python
# scraper.py — last line
asyncio.run(run(distance_miles=5, free=True))
```

```bash
python scraper.py
```

### Parameters

| Parameter | Type | Default | Options |
|---|---|---|---|
| `distance_miles` | `int` | `3` | `1, 3, 5, 7, 10, 15, 20, 30, 40, 50` |
| `free` | `bool` | `True` | `True` (free listings only) / `False` (all listings) |

---

## Sample Output

```python
{'price': 'Free', 'title': 'Outdoor patio set',        'time_posted': '2h ago',  'distance': '1.2 mi', 'neighborhood': 'Maple Heights'}
{'price': 'Free', 'title': "Kids bike — great condition", 'time_posted': '5h ago', 'distance': '2.8 mi', 'neighborhood': 'Riverside'}
{'price': '$25',  'title': 'Standing desk',             'time_posted': '1d ago',  'distance': '4.1 mi', 'neighborhood': 'Oak Park'}
```

---

## How It Works

1. **First run** — launches a visible Chromium window, logs into Nextdoor using your credentials, then saves session cookies to `cookies.json`.
2. **Subsequent runs** — loads the saved cookies and skips the login entirely.
3. Navigates to the Nextdoor Marketplace with the configured filters applied and extracts listing data directly from the DOM using Playwright's `page.evaluate()`.

---

## Disclaimer

This project is for **educational and personal use only**. Automated scraping may violate [Nextdoor's Terms of Service](https://help.nextdoor.com/s/article/Terms-of-Service). Use responsibly and at your own risk.

---

## License

[MIT](LICENSE)
