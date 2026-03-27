# Skills Documentation

This repository contains a comprehensive set of "skills"—structured documentation, scripts, and references that guide an AI agent in specialized domains like data analysis, machine learning, and scientific writing.

## Standardized Gold Standard

All skills in this repository follow a unified architectural standard:
1.  **Discovery-Optimized Frontmatter**: Descriptions start with "Use when..." to trigger correct loading by AI agents.
2.  **Mandatory Pre-flight Checks**: Resource detection logic to prevent OOM and system freezes.
3.  **API References**: Detailed `references/api-reference.md` files with formal signatures and docstrings extracted directly from the libraries.
4.  **Wall of Shame**: Common pitfalls and anti-patterns to avoid.

## Available Skills

### Core Workflow
#### Planning
- **brainstorming**: Turns ideas into fully formed designs and specs through collaborative dialogue.
- **writing-plans**: Generates bite-sized, TDD-ready implementation plans from specifications.

#### Execution & Testing
- **executing-plans**: Structured execution of implementation plans with review checkpoints.
- **systematic-debugging**: Root-cause focused debugging process for resolving technical issues reliably.
- **test-driven-development**: Strict Red-Green-Refactor workflow for robust code implementation.
- **verification-before-completion**: Mandatory evidence-based verification before claiming task completion.

#### Maintenance & Meta
- **using-superpowers**: Fundamental rules and priorities for skill discovery and application.
- **writing-skills**: TDD-based process for creating and refining persistent agent skills.

### Data Analysis
- **dask**: Scales pandas and NumPy workflows to larger-than-RAM datasets or clusters.
- **exploratory-data-analysis**: Performs comprehensive exploratory analysis on scientific and business data.
- **geopandas**: Analyzes geospatial vector data including shapefiles and GeoJSON.
- **matlab**: Provides matrix operations, data analysis, and scientific computing using MATLAB/Octave syntax.
- **numpy**: Performs numerical computing and vectorized math using arrays.
- **pandas**: Analyzes and transforms tabular data using DataFrames.
- **polars**: High-performance DataFrame library with a parallel Apache Arrow backend.
- **statistical-analysis**: Performs statistical testing, trend analysis, and business metric investigation.
- **statsmodels**: Implements statistical models for rigorous inference and diagnostics.

### Data Sources
- **elasticsearch**: Queries and indexes data using both Python client and ES|QL (cURL).
- **postgresql**: Newly added skill for interacting with PostgreSQL databases including complex queries.
- **query-optimization**: Best practices for optimizing SQL query performance.
- **s3**: Manages data storage and retrieval on AWS S3 and compatible services.
- **sql-queries**: Generates and optimizes SQL across major dialects (Postgres, Snowflake, BigQuery, DuckDB).
- **sql-syntax-and-functions**: Comprehensive SQL syntax and function guide across major databases.
- **sqlalchemy**: Provides database-agnostic access and ORM capabilities.

### Infrastructure Tools
- **data-context-extractor**: Extracts warehouse schemas and tribal knowledge to generate tailored data skills.
- **data-validation**: Enforces data quality, schemas, and analytical methodology.
- **get-available-resources**: Detects and reports available system resources (CPU, GPU, memory).
- **git**: Manages source code version control and collaborative workflows.
- **gitlab**: Expert guidance for using the GitLab CLI (glab) to manage issues, MRs, and pipelines.
- **jupyter**: Manages interactive development within Jupyter notebooks.
- **windows-cli**: Executes file and system operations using Windows cmd and PowerShell.

### Machine Learning
- **anomaly-detection**: Identifies unusual patterns or outliers in data.
- **pymc**: Builds and samples Bayesian models using probabilistic programming.
- **pytorch-lightning**: Organizes PyTorch code for scalable deep learning training.
- **scikit-learn**: Machine learning in Python (classification, regression, clustering).
- **stable-baselines3**: Provides production-ready reinforcement learning algorithms.
- **timesfm-forecasting**: Performs zero-shot time series forecasting using foundation models.
- **transformers**: Works with pre-trained transformer models for NLP, vision, and audio tasks.
- **umap-learn**: Performs non-linear dimensionality reduction for visualization and clustering.

### Networking & Security
- **log-parsing**: Parses structured and unstructured log files into DataFrames for analysis.
- **networkx**: Creates, analyzes, and visualizes complex networks and graphs.
- **scapy**: Interactive packet manipulation, sniffing, and crafting.
- **wireshark-extensions**: Develop custom Wireshark protocol dissectors using Lua.

### Python Development
- **cli-scripts**: Converts Python scripts into professional command-line tools.
- **debugging**: Step-by-step debugging for errors, bugs, or unexpected behavior.
- **dotenv**: Manages configuration and secrets using environment variables and .env files.
- **legacy-migration**: Migrates legacy codebases (C#, MATLAB) to modern Python (3.9+).
- **parallel-processing-pro**: Accelerates data tasks using Multithreading (I/O) and Multiprocessing (CPU).
- **pydantic**: Validates and manages data structures using Python type annotations.
- **pytest**: Writes and executes Python tests with clean syntax and powerful fixtures.
- **python-best-practices**: Enforces PEP-8, idiomatic Python, and formatting standards.
- **python-stdlib-pro**: Advanced usage of Python's standard library (Pathlib, Regex, JSON).
- **python2-migration**: Migrates legacy Python 2 code to Python 3.
- **refactoring**: Improves code quality and restructures Python codebases using automated tools.

### Scientific Workflow
- **peer-review**: Provides structured evaluation for manuscript and grant reviews.
- **research-summaries**: Generates technical and executive research summaries.
- **scholar-evaluation**: Systematically evaluates scholarly work across methodology and contribution.
- **scientific-brainstorming**: Facilitates creative research ideation and interdisciplinary exploration.
- **scientific-critical-thinking**: Evaluates scientific claims and evidence design validity.
- **scientific-schematics**: Creates publication-quality scientific diagrams and architectures.
- **scientific-slides**: Builds research-focused slide decks for conferences and seminars.
- **scientific-visualization**: Creates publication-ready multi-panel figures.
- **scientific-writing**: Drafts scientific manuscripts using a research-first two-stage process.

### Unstructured Data Processing
- **binary-data-parsing**: Parses and manipulates raw binary data and custom file formats.
- **bit-error-correction**: Detects and repairs corrupted data using error-correcting codes (ECC).
- **data-format-detection**: Identifies the format and encoding of unknown binary files.
- **docx**: Creates, reads, and manipulates Word (.docx) documents.
- **ffmpeg**: Processes and transforms audio, video, and image files.
- **pdf**: Extracts text, merges, splits, and manipulates PDF files.
- **pptx**: Creates, reads, and modifies PowerPoint (.pptx) presentations.
- **shapely**: Planar geometric manipulation and analysis.
- **xlsx**: Manages creation, editing, and analysis of spreadsheet files (.xlsx, .csv).

### Visualization
- **build-dashboard**: Builds interactive HTML dashboards with KPI cards, charts, and tables.
- **data-visualization**: Generates high-quality visualizations and provides design guidance.
- **plotly**: Creates interactive and publication-quality visualizations (Primary recommendation).
- **plotly-dash**: Builds interactive web dashboards and data applications.
- **seaborn**: Creates statistical visualizations with attractive defaults.

---
*For details on how to create or extend these skills, see the [writing-skills](skills/core-workflow/maintenance-and-meta/writing-skills/SKILL.md) documentation.*
