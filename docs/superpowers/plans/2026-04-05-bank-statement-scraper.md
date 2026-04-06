# Bank Statement Scraper Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a Python scraper using Playwright to extract 6 months of bank statements from a responsive, infinite-scrolling site after login.

**Architecture:** Playwright-based script using dynamic header mapping and an infinite scrolling loop with date-based termination.

**Tech Stack:** Python 3.x, Playwright (async), dateutil for date parsing.

---

### Task 1: Environment Setup
**Files:**
- Create: `requirements-scraper.txt`

- [ ] **Step 1: Define dependencies**
Add `playwright`, `pytest-playwright`, `python-dateutil` to `requirements-scraper.txt`.

- [ ] **Step 2: Install dependencies**
Run: `pip install -r requirements-scraper.txt`
Run: `playwright install chromium`

---

### Task 2: Core Scraper Implementation
**Files:**
- Create: `src/bank_scraper.py`

- [ ] **Step 1: Boilerplate and Imports**
Set up the `asyncio` loop and Playwright context.

- [ ] **Step 2: Authentication Logic**
Implement `async def login(page, username, password)` to fill form and click login.

- [ ] **Step 3: Dynamic Column Mapping**
Implement `async def get_column_indices(page)` to scan `<thead>` for 'Date', 'Amount', and 'Description'.

- [ ] **Step 4: Infinite Scroll with Date Filtering**
Implement `async def scrape_statements(page, lookback_months=6)` with a loop that scrolls and extracts rows until the date threshold is met.

- [ ] **Step 5: Row Parsing**
Extract data based on dynamic indices and convert to a list of dicts.

---

### Task 3: Execution Script
**Files:**
- Create: `main.py`

- [ ] **Step 1: Integration**
Combine functions into a main execution flow with error handling.
Pass 'user' and 'pass' as credentials.

---

### Task 4: Verification
**Files:**
- Create: `tests/test_bank_scraper.py` (Mocked)

- [ ] **Step 1: Write mock tests**
Test column mapping and date filtering with a sample HTML string.
