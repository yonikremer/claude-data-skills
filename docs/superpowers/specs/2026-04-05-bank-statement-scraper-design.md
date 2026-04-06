# Bank Statement Scraper Design

## Problem Statement
Scrape `https://example-bank.com/statements` after logging in. The site uses infinite scrolling and responsive design where table column indices may change. Extract 'Date', 'Amount', and 'Description' for the last 6 months.

## Proposed Approaches

### Option 1: Playwright for Python (Recommended)
- **Architecture**: Use Playwright's async API to control a Chromium browser.
- **Login**: Automated form submission with waits for navigation.
- **Infinite Scroll**: Loop with `window.scrollTo` or scrolling the specific table container until older rows appear.
- **Dynamic Columns**: Map column names from the `<thead>` to their indices at runtime.
- **Filtering**: Parse date strings and filter rows until reaching the 6-month threshold.
- **Pros**: Robust, fast, handled dynamic content and responsive layouts natively.

### Option 2: Selenium with Python
- **Architecture**: Use Selenium WebDriver with Chrome/Firefox.
- **Pros**: Familiar, extensive documentation.
- **Cons**: Slightly slower, boilerplate intensive for waiting/scrolling compared to Playwright.

## Recommended Approach: Playwright
Playwright offers a more modern and efficient API for handling dynamic content and asynchronous events, which is critical for infinite scrolling and responsive design checks.

## Component Design

### 1. Authentication Module
- Navigate to login page.
- Fill username and password.
- Click 'Login' and wait for redirection/success indicator.

### 2. Scroll & Load Module
- Identify the scrollable container.
- Implement a loop that scrolls down and waits for new row elements to appear.
- Terminate loop when data older than 6 months is detected.

### 3. Dynamic Column Mapper
- Locate the table header (`<th>` or equivalent).
- Store indices for 'Date', 'Amount', and 'Description'.
- Re-map if the layout changes (though usually mapping once per session/viewport is enough).

### 4. Data Extraction & Filtering
- Parse each row's columns based on mapped indices.
- Convert date strings to Python `datetime` objects.
- Stop when dates exceed the 6-month lookback period.

## Error Handling
- Handle login failures.
- Retry on network timeouts during scrolling.
- Graceful exit if table structure changes unexpectedly.

## Testing Strategy
- Mock the bank website with a local HTML file for integration tests.
- Unit test date parsing and column mapping functions.
