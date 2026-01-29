# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RD-Agent (R&D Agent) is an AI framework that automates research and development processes for data-driven scenarios. It implements a **two-agent evolving framework**:

- **Research Agent (R)**: Proposes new ideas, hypotheses, and experiment designs
- **Development Agent (D)**: Implements experiments, executes code, and collects feedback

The framework uses continuous evolution based on feedback and knowledge retention to improve performance over time.

### Key Scenarios

- **Quantitative Finance** (`rdagent/scenarios/qlib/`): Factor mining, model optimization, and strategy backtesting with Qlib integration
- **Data Science** (`rdagent/scenarios/data_science/`): Kaggle competitions, medical prediction, auto-ML
- **General Model** (`rdagent/scenarios/general_model/`): Paper-to-model extraction and implementation

---

## Development Commands

### Environment Setup

```bash
# Install in development mode with all dependencies
make dev

# Initialize Qlib environment (for quant scenarios)
make init-qlib-env

# Health check (validates Docker and environment)
rdagent health_check
```

### Code Quality

```bash
# Linting (run in order - isort before black)
make mypy      # Type checking (rdagent/core only)
make ruff      # Python linting
make isort     # Import sorting
make black     # Code formatting
make toml-sort # TOML file sorting
make lint      # Run all linters

# Auto-fix
make auto-lint # Auto-fix format issues (runs isort, black, toml-sort)
```

### Testing

```bash
# Run all tests
make test

# Run offline tests only (no API calls)
make test-offline

# Run single test
pytest test/path/to/test.py::test_function

# Run with coverage
python -m pytest --cov=rdagent
```

### Documentation

```bash
make docs       # Generate full documentation with reports
make docs-gen   # Build docs only
```

---

## Architecture

### Core Framework (`rdagent/core/`)

The core framework implements an evolving R&D methodology with these key components:

**`evolving_framework.py`** - Base classes for evolution:
- `EvolvableSubjects`: Objects that can be evolved (factors, models, etc.)
- `EvoStep`: Single evolution step tracking (subjects, knowledge, feedback)
- `EvolvingStrategy`: Abstract strategy for how subjects evolve
- `RAGStrategy`: Retrieval Augmented Generation for knowledge management

**`proposal.py`** - Hypothesis generation and experiment proposal

**`developer.py`** - Development agent implementation

**`evaluation.py`** - Feedback collection and evaluation mechanisms

**`knowledge_base.py`** - Persistent knowledge storage and retrieval

**`conf.py`** - Configuration management using Pydantic settings

### Application Structure (`rdagent/app/`)

Each scenario has a corresponding app module:

- **`qlib_rd_loop/`**: Quantitative finance scenarios
  - `quant.py` - Full factor-model co-optimization
  - `factor.py` - Factor evolution only
  - `model.py` - Model evolution only
  - `factor_from_report.py` - Extract factors from financial reports

- **`data_science/`**: General data science scenarios
  - `loop.py` - Main data science loop

- **`general_model/`**: Research copilot scenarios
  - `general_model.py` - Model extraction from papers

### Scenarios (`rdagent/scenarios/`)

**`qlib/`** - Quantitative finance with Qlib:
- Factor mining and evolution
- Model optimization and backtesting
- Financial report analysis

**`data_science/`** - General ML:
- Kaggle competition automation
- Medical prediction models
- Feature engineering

**`general_model/`** - Research copilot:
- Paper-to-model extraction
- Research assistance

### Entry Points (`rdagent/app/cli.py`)

```bash
# Quantitative finance
rdagent fin_quant           # Full factor-model co-optimization
rdagent fin_factor          # Factor evolution only
rdagent fin_model           # Model evolution only
rdagent fin_factor_report --report-folder=<path>  # Extract factors from reports

# General data science
rdagent general_model <paper_url>       # Implement model from paper
rdagent data_science --competition <name>  # Kaggle/auto-ML scenario

# Utilities
rdagent health_check          # Validate environment
rdagent ui --port 19899 --log-dir log/  # View experiment logs (web UI)
rdagent ui --data_science     # View data science scenario logs
```

---

## Configuration

Configuration is handled via `.env` file in the project root:

```bash
# LLM configuration (LiteLLM backend)
CHAT_MODEL=gpt-4o
EMBEDDING_MODEL=text-embedding-3-small
OPENAI_API_BASE=<your_api_base>
OPENAI_API_KEY=<your_key>

# Or separate providers
CHAT_MODEL=deepseek/deepseek-chat
DEEPSEEK_API_KEY=<key>
EMBEDDING_MODEL=litellm_proxy/BAAI/bge-m3
LITELLM_PROXY_API_KEY=<key>
LITELLM_PROXY_API_BASE=https://api.siliconflow.cn/v1

# For reasoning models (o1, o3, etc.)
REASONING_THINK_RM=True
```

---

## Key Design Patterns

### Multi-Agent Coordination

- **Strategy Pattern**: Pluggable evolving strategies for different scenarios
- **Template Method**: Base workflow with customizable steps
- **Observer Pattern**: Feedback collection and propagation

### Knowledge Management

- **RAG (Retrieval Augmented Generation)**: Knowledge querying and generation
- **Persistent Knowledge Bases**: Learning retained across sessions
- **Evolving Trace**: Historical experiment results guide future proposals

### Configuration-Driven

- **Environment Variables**: LLM backend configuration via `.env`
- **YAML Configs**: Scenario-specific experiment settings
- **Pydantic Settings**: Type-safe configuration management

---

## Important Notes

- **Linux Only**: RD-Agent currently only supports Linux
- **Docker Required**: Most scenarios require Docker to be installed
- **Python Version**: Requires Python 3.10 or 3.11
- **API Keys**: Configure LLM keys in `.env` before running experiments
- **Port Conflicts**: Default UI port is 19899; check with `rdagent health_check --no-check-env --no-check-docker`

---

## Workflow Overview

The evolving R&D loop:

```
Hypothesis → Experiment Design → Code Implementation → Execution → Feedback → Knowledge Update → Repeat
```

1. **Research Agent** proposes new ideas based on knowledge and feedback
2. **Development Agent** implements and executes experiments
3. **Evaluation** collects metrics and feedback
4. **Knowledge Base** stores learnings for future iterations
5. **Evolution** improves performance over time

---

## Common Tasks

### Run Quant Experiment

```bash
cd /home/mind/quant/RD-Agent
rdagent fin_quant  # Runs factor-model co-optimization loop

# Monitor results
rdagent ui --log-dir log/
```

### Debug Failed Experiment

1. Check logs in `log/` directory
2. Use `rdagent ui` for visual inspection
3. Review generated code in `git_ignore_folder/`
4. Adjust configuration in `.env` or scenario config files

### Sync with Upstream

```bash
git fetch github && git merge github/main
```

---

## References

- **Documentation**: https://rdagent.readthedocs.io/
- **Live Demo**: https://rdagent.azurewebsites.net/
- **Technical Report**: https://arxiv.org/abs/2505.14738
- **Qlib**: https://qlib.readthedocs.io/
