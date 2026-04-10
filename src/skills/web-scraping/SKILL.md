---
name: pro-web-scraping
description: Use when building industrial-grade scrapers for complex sites (e.g., Coursera, LinkedIn) with aggressive anti-bot (Cloudflare), dynamic JS rendering, infinite scroll, login/session management, or giant/brittle HTML blobs.
---

# Pro Web Scraping

## Domain Fundamentals

Modern web scraping at scale requires navigating three primary battlefronts:
1.  **Anti-Bot Warfare**: WAFs (Cloudflare, Akamai, Datadome) use TLS/HTTP2 fingerprinting and behavioral analysis to block automated tools.
2.  **JS-Heavy SPA Architectures**: Data is not in the initial HTML; it's rendered asynchronously via React/Angular/Vue.
3.  **Selector Fragility**: Minified CSS and responsive designs break static CSS/XPath selectors.

## Tool Selection Strategy

| Requirement | Recommendation | Tool |
| :--- | :--- | :--- |
| **Simple / Static** | Fast, light | `requests` + `BeautifulSoup4` |
| **High Stealth / JS** | Adaptive & Protected | `Scrapling` (StealthyFetcher) |
| **Complex Interactivity** | Full Browser Control | `Playwright` (Async) |
| **Login / Session** | Persistent browser state | `Playwright` + `storage_state` |
| **Industrial / Scale** | Multi-strategy chain | **The Scrapling + Playwright Orchestration** |

## Core Workflows

### 1. Stealth & Anti-Bot Bypass
Use `Scrapling` for its built-in spoofing of TLS and browser fingerprints.

```python
from scrapling.fetchers import StealthyFetcher

# Bypassing Cloudflare Turnstile & other WAFs
page = StealthyFetcher.fetch(
    "https://example.com/protected",
    solve_cloudflare=True,
    network_idle=True, # Wait for JS rendering
    headless=True
)
print(page.css("h1").first.text)
```

### 2. Complex Interactivity (Playwright)
Use `Playwright` for infinite scrolling, logins, and complex "Load More" triggers.

```python
from playwright.async_api import async_playwright

async def scroll_to_bottom(page):
    last_height = await page.evaluate("document.body.scrollHeight")
    while True:
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(2000) # Wait for network
        new_height = await page.evaluate("document.body.scrollHeight")
        if new_height == last_height: break
        last_height = new_height

# Login with state persistence
# context = await browser.new_context(storage_state="auth.json")
```

### 3. Discovery & Extraction from Giant HTML
When Faced with a "giant blob" (5MB+) of minified HTML:
1.  **Marker Discovery**: Use `find_by_text()` or `find_by_regex()` on a Scrapling `Adaptor` to find a known item.
2.  **Structural Navigation**: Use `.parent` and `.children` to navigate from the marker to the repeating container.
3.  **Generated Selectors**: Use `.generate_css_selector` on a `Selector` to identify a robust path.
4.  **Mass Extraction**: Use `.find_similar()` on the discovered container to extract all other identical items on the page.

### 4. Advanced Orchestration: The "Strategy Chain"
For high-value, high-complexity targets (e.g., Coursera):
-   **Content Readiness**: Wait for *content markers* (e.g., `div.rc-Question`), not just `onload`.
-   **Fallback Chain**: Link tags -> DOM inspection (`<video>`) -> Network/Manifest analysis (`.m3u8`) -> External tools (`yt-dlp`).
-   **DOM Sanitization**: Use `execute_script` to remove sidebars, scripts, and popups before extraction to reduce "noise."

## AI-Ready Extraction

-   **Markdown Conversion**: Convert extracted HTML segments to Markdown (e.g., via `markdownify`) to reduce tokens and improve LLM parsing accuracy.
-   **Selective Context**: Instead of the full blob, pass only the `html_content` of relevant containers to the AI.

## Wall of Shame (Pitfalls & Gotchas)

-   **Selectors vs Selector**: `page.css()` returns a `Selectors` object (list-like). You MUST use `.first` or indexing `[0]` to get a single `Selector` object before accessing `.text`.
-   **Text Extraction**: Use the `.text` attribute (not a method `.text()`) on a `Selector` object.
-   **Adaptive Initialization**: Adaptive tracking MUST be enabled during initialization of the fetcher/adaptor (`adaptive=True`), otherwise `auto_save` and `adaptive` arguments on `css()` calls will be ignored.
-   **Selector Generation Properties**: `.generate_css_selector` and `.generate_xpath_selector` are **string properties**, not methods. Do not call them with `()`.
-   **Brittle Selectors**: Avoid `div > div > span:nth-child(3)`. Use stable `data-testid`, ARIA roles, or Scrapling's `find_by_text` marker pattern.
-   **No Stealth**: Running `headless=True` in standard Playwright without `playwright-stealth` (detected easily). Use `Scrapling` for better defaults.
-   **Wait Strategy**: Avoid `time.sleep()`. Use `page.wait_for_selector()` or Scrapling's `network_idle=True`.
-   **Missing Dependencies**: Forgetting `playwright install chromium` after setting up.

## References
- [Official Scrapling Documentation](https://scrapling.readthedocs.io/)
- [Playwright Python API](https://playwright.dev/python/docs/intro)
- [Official Kaggle API](https://github.com/Kaggle/kaggle-api)
- `src/skills/web-scraping/references/scrapling-specs.md` — Deep dive into Scrapling's adaptive internals.
- `src/skills/web-scraping/references/interactive.md` — Advanced Playwright patterns for heavy interactivity.
- `src/skills/web-scraping/scripts/templates/` — Scrapling and Playwright boilerplates.
