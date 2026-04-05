---
name: web-scraping-pro
description: Use when scraping data from websites with dynamic content (JS-heavy), interactive elements (Load More, Scroll), or requiring login/session management. High-fidelity extraction, stealth mode, and robust handling of varied HTML structures.
---

# Web Scraping Pro

Unified guide for professional data extraction from the web, with a focus on interactivity, stealth, and robust parsing.

## ⚠️ Pre-flight: Tool Selection

| Scenario                   | Recommendation      | Tool                                |
|----------------------------|---------------------|-------------------------------------|
| **Simple API/Static HTML** | Fast, light         | `requests` + `BeautifulSoup4`       |
| **JS-Heavy / AJAX**        | Browser automation  | `Playwright` (Async)                |
| **Login / Session**        | Persistent sessions | `Playwright` + `storage_state`      |
| **Bot Detection**          | High-fidelity       | `Playwright` + `playwright-stealth` |

---

## 1. Interactive Scraping (Playwright)

Use for modern, reactive websites where data is not in the initial HTML.

### Core Idioms: Interactivity

- **Stealth**: Always use `playwright-stealth` to bypass basic bot detection.
- **Waiting**: NEVER use `time.sleep()`. Use `page.wait_for_selector()` or `page.wait_for_load_state()`.
- **Session Persistence**: Save and load `storage_state` to avoid repetitive (and blockable) logins.

```python
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async


async def scrape_dynamic_content():
    async with async_playwright() as p:
        # Launch with stealth
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0...")
        page = await context.new_page()
        await stealth_async(page)  # Apply stealth

        # Handle Session (Load)
        # await context.add_cookies(loaded_cookies)

        await page.goto("https://example.com/dynamic")

        # Click "Load More" until gone
        while True:
            button = page.locator('button:has-text("Load More")')
            if await button.is_visible():
                await button.click()
                await page.wait_for_load_state("networkidle")
            else:
                break
```

---

## 2. Robust Parsing & Selectors

Avoid fragile CSS paths. Modern sites use responsive designs where structures change.

### The "Stable Selector" Hierarchy

1. **Data Attributes**: `[data-testid="product-name"]` (Most stable).
2. **ARIA Roles**: `role="row"`, `role="cell"` (Semantically stable).
3. **Text-based**: `page.get_by_text("Price")` (User-facing stable).
4. **Layout-based**: `page.locator("label:has-text('Date') + input")` (Relatively stable).

### Dynamic Column Mapping

When scraping tables with changing column orders, map indices at runtime:

```python
# Map indices from header
headers = await page.query_selector_all('thead th')
column_map = {(await h.inner_text()).strip(): i for i, h in enumerate(headers)}

# Use map to extract from rows
rows = await page.query_selector_all('tbody tr')
for row in rows:
    cells = await row.query_selector_all('td')
    date = await cells[column_map['Date']].inner_text()
```

---

## 3. Handling Interactions

### Infinite Scroll

```python
async def scroll_to_bottom(page):
    last_height = await page.evaluate("document.body.scrollHeight")
    while True:
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(2000)  # Wait for load
        new_height = await page.evaluate("document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
```

### Login with Storage State

```python
# 1. Login once and save state
await page.fill("#user", "my_user")
await page.click("#login")
await context.storage_state(path="auth.json")

# 2. Reuse state in future sessions
context = await browser.new_context(storage_state="auth.json")
```

---

## 🛠️ Common Pitfalls (The "Wall of Shame")

1. **Wait Strategy**: Using `time.sleep(5)` instead of `page.wait_for_selector()`.
2. **Headless Detection**: Running `headless=True` without stealth or user-agent spoofing.
3. **Hardcoded Indices**: Using `cells[3]` for "Price" when the index might change.
4. **Blocking**: Forgetting to set a reasonable `timeout` (default is 30s) or failing to handle `Try/Except` for
   timeouts.
5. **No Cleanup**: Failing to `await browser.close()` on exception, leaving "zombie" browser processes.

## References

- `skills/unstructured-data-processing/web-scraping-pro/references/interactive.md` — Advanced Playwright patterns.
- `skills/unstructured-data-processing/web-scraping-pro/scripts/templates/` — Scrapy and Playwright boilerplates.
