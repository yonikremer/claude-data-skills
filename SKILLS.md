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

#### Meta & Discovery
- **using-superpowers**: Fundamental rules and priorities for skill discovery and application.

### Learning and Skill Building
- **tech-explorer**: Researches, tests, and masters unfamiliar technologies (libraries, APIs, databases) to create comprehensive, "Gold Standard" skills.
- **writing-skills**: TDD-based process for creating and refining persistent agent skills.
- **api-skill-creator**: Transforms API documentation (Swagger, Wiki, etc.) into reusable skills for internal or external services.
- **database-skill-creator**: Transforms database structures (schemas, relationships) into reusable skills for specific data sources.

### Data Analysis
- **data-analysis-pro**: Consolidated power-user guide for NumPy, Pandas, and Polars. Unified strategy for scaling from KB to 100GB+.
- **exploratory-data-analysis**: Performs comprehensive exploratory analysis on scientific and business data.
- **geopandas**: Analyzes geospatial vector data including shapefiles and GeoJSON.
- **matlab**: Provides matrix operations, data analysis, and scientific computing using MATLAB/Octave syntax.
- **statistical-analysis**: Performs statistical testing, trend analysis, and business metric investigation.
- **statsmodels**: Implements statistical models for rigorous inference and diagnostics.

### Data Sources
- **database-pro**: Consolidated expert guide for SQL (queries/schemas), SQLAlchemy (ORM), PostgreSQL, Elasticsearch (search/indexing), and S3 (object storage).

### Infrastructure Tools
- **data-context-extractor**: Extracts warehouse schemas and tribal knowledge to generate tailored data skills.
- **data-validation**: Enforces data quality, schemas, and analytical methodology.
- **get-available-resources**: Detects and reports available system resources (CPU, GPU, memory).
- **git**: Manages source code version control and collaborative workflows.
- **gitlab**: Expert guidance for using the GitLab CLI (glab) to manage issues, MRs, and pipelines.
- **jupyter**: Manages interactive development within Jupyter notebooks.
- **windows-cli**: Executes file and system operations using Windows cmd and PowerShell.

### Machine Learning
- **ml-classical**: Consolidated expert guide for Scikit-Learn, UMAP (dimensionality reduction), and Anomaly Detection.
- **ml-deep-learning**: Consolidated expert guide for PyTorch Lightning (scalable training) and Transformers (Hugging Face).
- **pymc**: Builds and samples Bayesian models using probabilistic programming.
- **stable-baselines3**: Provides production-ready reinforcement learning algorithms.
- **timesfm-forecasting**: Performs zero-shot time series forecasting using foundation models.

### Networking & Security
- **log-parsing**: Parses structured and unstructured log files into DataFrames for analysis.
- **networkx**: Creates, analyzes, and visualizes complex networks and graphs.
- **scapy**: Interactive packet manipulation, sniffing, and crafting.
- **wireshark-extensions**: Develop custom Wireshark protocol dissectors using Lua.

### Python Development
- **python-core-pro**: Consolidated expert guide for Best Practices (PEP-8), Pydantic (Type Safety), Pytest (Testing), and Parallel Processing.
- **legacy-migration-suite**: Consolidated guide for migrating from Python 2, C#, or MATLAB to modern Python (3.9+).

### Scientific Workflow
- **scientific-research-suite**: Consolidated expert guide for the complete scientific lifecycle: brainstorming, research design, critical thinking, writing (IMRAD), and peer review.

### Unstructured Data Processing
- **binary-data-parsing**: Parses and manipulates raw binary data and custom file formats.
- **bit-error-correction**: Detects and repairs corrupted data using error-correcting codes (ECC).
- **data-format-detection**: Identifies the format and encoding of unknown binary files.
- **document-processing-pro**: Consolidated expert guide for PDF, Word (DOCX), Excel (XLSX), and PowerPoint (PPTX).
- **ffmpeg**: Processes and transforms audio, video, and image files.
- **shapely**: Planar geometric manipulation and analysis.

### Visualization
- **visualization-pro**: Consolidated expert guide for Plotly (interactive), Dash (dashboards), and Seaborn (static stats).

---
*For details on how to create or extend these skills, see the [writing-skills](src/skills/learning-and-skill-building/writing-skills/SKILL.md) documentation.*
