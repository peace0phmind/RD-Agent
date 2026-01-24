# Exhaustive Search - Phase 1 User Guide

## Overview

Phase 1 implements systematic single-factor scanning to evaluate the predictive power of individual factors.

## Features

- **Systematic Testing**: Test 50+ factors from multiple sources
- **Experiment Tracking**: All results stored in SQLite database
- **Automated Reporting**: Generate markdown and CSV reports
- **SOTA Comparison**: Automatic comparison with current best results

## Quick Start

### Basic Usage

```bash
# Activate environment
conda activate quant

# Run Layer 1 exhaustive search
rdagent exhaustive_search --layers 1

# Run with higher parallelism
rdagent exhaustive_search --layers 1 --max_parallel 8
```

### Python API

```python
from rdagent.app.qlib_rd_loop.exhaustive_search import ExhaustiveSearchLoop
import asyncio

loop = ExhaustiveSearchLoop(
    layers="1",
    max_parallel=4,
    results_dir="results/my_experiment"
)

asyncio.run(loop.run_full_pipeline())
```

## Results

After completion, find results in the `results/` directory:

- `experiments.db`: SQLite database with all experiments
- `layer1_report.md`: Summary report
- `top_factors.csv`: Top factors in CSV format

## Success Criteria

Phase 1 succeeds if:
- ✅ 50+ factors tested
- ✅ Top 10 factors identified
- ✅ Best IC > 0.0985 (current SOTA)

## Next Steps

After Phase 1, proceed to:
- Phase 2: Factor combination optimization
- Phase 3: Model and hyperparameter optimization
