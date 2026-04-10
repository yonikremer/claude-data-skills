# Tech Specs: Scrapling Library

## Overview
Scrapling is an adaptive, high-performance Python web scraping framework designed to handle everything from single requests to large-scale crawls. It excels at bypassing anti-bot protections and maintaining resilient selectors through "adaptive" element tracking.

- **GitHub**: [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling)
- **Documentation**: [scrapling.readthedocs.io](https://scrapling.readthedocs.io/)
- **Installation**: `pip install scrapling` (use `pip install "scrapling[all]"` for full browser capabilities).

## Domain Fundamentals

### Anti-Bot Protection (Stealth)
Websites use various techniques to detect and block automated scrapers:
- **TLS Fingerprinting**: Identifying the client's TLS stack (e.g., Python `requests` vs. a real browser).
- **HTTP/2 Fingerprinting**: Analyzing how the client handles HTTP/2 features.
- **Canvas/WebGL Fingerprinting**: Detecting inconsistencies in browser rendering.
- **Behavioral Analysis**: Monitoring mouse movements, keystrokes, and navigation patterns.
- **WAFs (Web Application Firewalls)**: Systems like Cloudflare, Akamai, and Datadome that intercept and block suspicious traffic.

`StealthyFetcher` in Scrapling is designed to spoof these fingerprints and bypass these protections out-of-the-box.

### Adaptive Element Tracking (Resilient Selectors)
Standard CSS or XPath selectors are brittle; a small change in a website's HTML structure can break them.
- **Fingerprinting Elements**: Scrapling can "learn" an element by saving its context, attributes, and surrounding structure.
- **Similarity Algorithms**: If the original selector fails, Scrapling uses similarity algorithms to find the "best match" for the fingerprinted element in the new DOM.
- **Self-Healing**: This "self-healing" capability reduces maintenance overhead for long-running scrapers.

## Core API Classes & Usage

### 1. StealthyFetcher
Used for requests that need to bypass anti-bot systems.
- `StealthyFetcher.fetch(url, ...)`: One-off stealthy request.
- `StealthySession`: Maintains cookies and state across multiple stealthy requests.
- **Key Parameters**: `headless=True`, `solve_cloudflare=True`, `network_idle=True`, `google_search=True`.

### 2. AsyncFetcher
For high-performance, concurrent scraping.
- `AsyncStealthySession`: Asynchronous session with a browser tab pool.
- `max_pages`: Limits the number of concurrent pages/tabs.
- `session.get_pool_stats()`: Monitor pool usage.

### 3. Adaptive Selectors
- `page.css(selector, adaptive=True)`: Uses adaptive tracking.
- `auto_save=True`: Saves the element's fingerprint for future use.
- `element.find_similar()`: Manually find similar elements.

## AI Integration (MCP Server)
- **Model Context Protocol (MCP)**: Scrapling includes a built-in MCP server for AI-assisted scraping.
- **Benefit**: Allows AI agents (e.g., Claude, Cursor) to use Scrapling as a tool, extracting only necessary data and saving on token costs.
- **Installation**: `pip install "scrapling[ai]"`.
