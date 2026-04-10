# Advanced Interactive Scraping with Playwright

This guide covers advanced patterns for complex interactivity, including shadow DOM, iframes, and file uploads.

## 1. Handling Shadow DOM

Playwright supports shadow DOM by default in CSS selectors, but some complex sites might require explicit piercing.

```python
# Select an element inside a shadow-root
page.locator('my-component >> .internal-button')
```

## 2. iFrames (e.g., Bank Logins, Ad-free Views)

```python
# Access an iframe by its name or URL
frame = page.frame(name="login-frame")
# Or by selector
frame = page.frame_locator("#frame-id")

await frame.fill("#user", "user")
await frame.click("#submit")
```

## 3. File Uploads

```python
# Upload a file to an <input type="file">
await page.set_input_files('input[type="file"]', 'path/to/file.pdf')

# Or if you need to trigger a click first
async with page.expect_file_chooser() as fc_info:
    await page.click('#upload-button')
file_chooser = await fc_info.value
await file_chooser.set_files('path/to/file.pdf')
```

## 4. Bypassing Bot Detection (Advanced)

Beyond `playwright-stealth`:
- **Wait for Realism**: Don't click instantly. Add small random delays between actions.
- **Viewport**: Use realistic viewports.
- **Geolocation**: Some sites require matching geolocation to IP.

```python
context = await browser.new_context(
    viewport={'width': 1920, 'height': 1080},
    user_agent='...',
    locale='en-US',
    timezone_id='America/New_York',
    geolocation={'longitude': -74.006, 'latitude': 40.7128},
    permissions=['geolocation']
)
```
