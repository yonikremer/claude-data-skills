# Skills Documentation

This repository contains a curated set of "skills"—structured documentation, scripts, and references that guide an
AI agent in specialized domains like data analysis, machine learning, and scientific computing.

## Standardized Gold Standard

All skills in this repository follow a unified architectural standard:

1. **Discovery-Optimized Frontmatter**: Descriptions start with "Use when..." to trigger correct loading by AI agents.
2. **Mandatory Pre-flight Checks**: Resource detection logic to prevent OOM and system freezes.
3. **API References**: Detailed `references/` files with formal signatures, docstrings, and domain context.
4. **Wall of Shame**: Common pitfalls and anti-patterns to avoid.

## Available Skills

### Data Analysis

- **cupy-signal**: GPU-accelerated signal processing using `cupyx.scipy.signal`. A high-performance drop-in replacement
  for `scipy.signal` on NVIDIA (CUDA) and AMD (ROCm) GPUs.
- **exploratory-data-analysis**: Comprehensive exploratory analysis on scientific and business data, including structural
  analysis, data quality checks, profiling, and categorical hierarchies.
- **geopandas**: Analysis of geospatial vector data (Shapefiles, GeoJSON, GeoPackage), including spatial joins,
  coordinate transformations, and choropleth mapping.
- **matlab**: Matrix operations, data analysis, and scientific computing using MATLAB/Octave syntax. Useful for writing
  scientific scripts or converting between MATLAB and Python.
- **statsmodels**: Statistical models for rigorous inference, hypothesis testing, and diagnostics. Covers econometrics,
  time series (ARIMA), and detailed coefficient tables.

### Infrastructure Tools

- **data-context-extractor**: Extracts warehouse schemas and tribal knowledge to generate tailored data skills.
- **get-available-resources**: Detects and reports available system resources (CPU, GPU, memory) to inform computational
  strategy before intensive tasks.

### Learning and Skill Building

- **api-skill-creator**: Transforms API documentation (Swagger, Wiki, Confluence, etc.) into reusable skills for
  internal or external services.
- **database-skill-creator**: Transforms database structures (schemas, relationships) into reusable skills for specific
  data sources.
- **tech-explorer**: Researches, tests, and masters unfamiliar technologies (libraries, APIs, databases) to create
  comprehensive, empirical skills.
- **writing-skills**: TDD-based process for creating, editing, and verifying persistent agent skills.

### Machine Learning

- **pymc**: Builds and samples Bayesian models using probabilistic programming.
- **stable-baselines3**: Provides production-ready reinforcement learning algorithms.
- **timesfm-forecasting**: Zero-shot time series forecasting using Google's TimesFM foundation models.

### Networking & Security

- **networking-security-suite**: Glue logic for end-to-end network security analysis, from PCAP triage to topology
  mapping and deep packet inspection.
- **networkx**: Creates, analyzes, and visualizes complex networks and graphs.
- **scapy**: Interactive packet manipulation, sniffing, and crafting for network discovery and protocol research.
- **wireshark-extensions**: Develops custom Wireshark protocol dissectors using Lua.
- **wireshark-pro**: Analyzes network traffic, handles large PCAP files, and extracts packet data programmatically.

### Unstructured Data Processing

- **binary-data-parsing**: Parses and manipulates raw binary data and custom file formats.
- **bit-error-correction**: Detects and repairs corrupted data using error-correcting codes (ECC).
- **data-format-detection**: Identifies the format and encoding of unknown binary files or raw bytes.
- **shapely**: Planar geometric manipulation and spatial analysis (buffering, intersections, spatial predicates).

### Web Scraping

- **pro-web-scraping**: Industrial-grade scrapers for complex sites with aggressive anti-bot protection, dynamic JS
  rendering, infinite scroll, login/session management, or brittle HTML.

---

*For details on how to create or extend these skills, see
`src/skills/learning-and-skill-building/writing-skills/SKILL.md`.*
