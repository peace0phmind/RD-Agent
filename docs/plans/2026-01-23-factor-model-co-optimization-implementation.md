# Factor-Model Co-optimization Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build and execute an automated factor-model co-optimization workflow using RD-Agent that achieves IC > 0.11, annual returns > 5%, max drawdown < 10%, and cross-period stability.

**Architecture:** Three-phase iterative co-optimization approach - Phase 1 evolves factors with fixed model, Phase 2 optimizes models with fixed best factors, Phase 3 performs joint fine-tuning of factor weights and model hyperparameters.

**Tech Stack:** RD-Agent framework, Qlib quantitative platform, Python 3.11, LightGBM/MLP/HIST models, YAML configuration

---

## Task 1: Setup Experiment Infrastructure

**Files:**
- Create: `docs/experiments/2026-01-23-co-optimization/README.md`
- Create: `docs/experiments/2026-01-23-co-optimization/real_time_log.md`
- Create: `docs/experiments/2026-01-23-co-optimization/loop_summary.csv`
- Create: `docs/experiments/2026-01-23-co-optimization/decision_log.md`
- Create: `docs/experiments/2026-01-23-co-optimization/lessons_learned.md`
- Create: `git_ignore_folder/experiment_tracking/track_experiment.sh`

**Step 1: Create experiment directory structure**

```bash
mkdir -p docs/experiments/2026-01-23-co-optimization
mkdir -p git_ignore_folder/experiment_tracking
mkdir -p log/co-optimization-exp
```

**Step 2: Create experiment README**

Write to `docs/experiments/2026-01-23-co-optimization/README.md`:

```markdown
# Factor-Model Co-optimization Experiment

**Date**: 2026-01-23
**Objective**: Achieve IC > 0.11, Returns > 5%, Drawdown < 10%
**Approach**: Iterative co-optimization (3-phase)

## Quick Links

- [Real-time Log](real_time_log.md) - Live experiment updates
- [Loop Summary](loop_summary.csv) - Quantitative results per loop
- [Decision Log](decision_log.md) - Key decisions and rationale
- [Lessons Learned](lessons_learned.md) - Insights for future experiments

## Experiment Structure

```
Phase 1 (Loop 1-5): Factor Evolution with Fixed Model
  ↓
Phase 2 (Loop 6-10): Model Optimization with Fixed Factors
  ↓
Phase 3 (Loop 11-15): Joint Fine-tuning
```

## Baseline

- Starting IC: 0.102 (Price_Distance_Z factor)
- Starting Returns: -2.42%
- Model: LightGBM SOTA

## Target

- IC: > 0.11 (+7.8% improvement)
- Returns: > 5% (turn positive)
- Drawdown: < 10%
```

**Step 3: Initialize loop summary CSV**

Write to `docs/experiments/2026-01-23-co-optimization/loop_summary.csv`:

```csv
Loop,Phase,Time,Factor_Count,Primary_Factor,Model,IC,IC_IR,Ann_Return,Max_Drawdown,Sharpe,Notes
0,Baseline,08:00,3,Price_Distance_Z,LightGBM,0.102,0.45,-2.42%,0.00%,-0.25,Baseline from previous experiment
```

**Step 4: Initialize decision log**

Write to `docs/experiments/2026-01-23-co-optimization/decision_log.md`:

```markdown
# Key Decisions Log

## Decision 0: Experiment Approach

**Time**: 2026-01-23 (Planning phase)
**Context**: Need to find effective factor-model combination with balanced IC and returns

**Options**:
- A: Iterative co-optimization (factor → model → joint)
- B: Synchronous joint evolution (factor + model together)
- C: Hierarchical (factor then model)

**Selection**: A (Iterative co-optimization)
**Rationale**:
- Computationally efficient (2-3 hours vs 4-6 hours)
- Easier to debug and trace issues
- Each component gets fully optimized
- Proven effective in prior experiments

**Expected Outcome**: IC > 0.11 and Returns > 5% within 15 loops
```

**Step 5: Initialize real-time log**

Write to `docs/experiments/2026-01-23-co-optimization/real_time_log.md`:

```markdown
# Factor-Model Co-optimization Real-time Log

**Experiment ID**: co-optimization-2026-01-23
**Start Time**: 2026-01-23 [TBD]
**Target**: IC > 0.11, Returns > 5%, Drawdown < 10%, Stable across 2017-2020

---

## Phase 1: Factor Evolution (Loop 1-5)

**Objective**: Find factor combination with IC > 0.11
**Fixed Model**: LightGBM (SOTA configuration)
**Starting Point**: Price_Distance_Z (IC: 0.102)

### Loop 0 - Baseline Measurement
**Time**: [Pending]
**Configuration**:
- Factors: Price_Distance_Z_5D, Price_Distance_Z_10D, Price_Distance_Z_20D
- Model: LightGBM with Qlib SOTA config
- Data: Train (2008-2014), Valid (2015-2016), Test (2017-2020)

**Results**: [Pending execution]

**Analysis**: [Pending]

---

[Subsequent loops will be appended here as experiment runs]
```

**Step 6: Create tracking script**

Write to `git_ignore_folder/experiment_tracking/track_experiment.sh`:

```bash
#!/bin/bash
# Experiment tracking utility
# Usage: ./track_experiment.sh <loop_number> <phase> <experiment_dir>

LOOP_NUM=$1
PHASE=$2
EXP_DIR=$3
LOG_FILE="docs/experiments/2026-01-23-co-optimization/real_time_log.md"
CSV_FILE="docs/experiments/2026-01-23-co-optimization/loop_summary.csv"

echo "Extracting results for Loop $LOOP_NUM ($PHASE)..."

# Extract IC
IC=$(grep -r "IC of Current Result" "$EXP_DIR/Loop_$LOOP_NUM" 2>/dev/null | tail -1 | awk '{print $NF}' || echo "N/A")

# Extract annual return
ANN_RETURN=$(grep -r "annualized_return" "$EXP_DIR/Loop_$LOOP_NUM" 2>/dev/null | grep -oP '\-?\d+\.\d+' | head -1 || echo "N/A")

# Extract max drawdown
DRAWDOWN=$(grep -r "max_drawdown" "$EXP_DIR/Loop_$LOOP_NUM" 2>/dev/null | grep -oP '\-?\d+\.\d+' | head -1 || echo "N/A")

# Append to CSV
TIMESTAMP=$(date +%H:%M)
echo "$LOOP_NUM,$PHASE,$TIMESTAMP,,$exp_id,LightGBM,$IC,,$ANN_RETURN,$DRAWDOWN," >> "$CSV_FILE"

# Append to real-time log
cat >> "$LOG_FILE" << EOF

### Loop $LOOP_NUM - $PHASE
**Time**: $(date '+%Y-%m-%d %H:%M')
**Experiment Directory**: $EXP_DIR

**Results**:
- IC: $IC
- Annual Return: $ANN_RETURN%
- Max Drawdown: $DRAWDOWN%

**Analysis**: [To be filled manually]

EOF

echo "Results logged. Next steps:"
echo "1. Review results in $LOG_FILE"
echo "2. Update analysis section manually"
echo "3. Document key decisions in decision_log.md"
```

**Step 7: Make tracking script executable**

```bash
chmod +x git_ignore_folder/experiment_tracking/track_experiment.sh
```

**Step 8: Commit experiment infrastructure**

```bash
git add docs/experiments/2026-01-23-co-optimization/ git_ignore_folder/experiment_tracking/
git commit -m "feat: add experiment tracking infrastructure for factor-model co-optimization

- Create directory structure for experiment documentation
- Initialize tracking templates (real-time log, decision log, summary CSV)
- Add automated tracking script for result extraction
```

---

## Task 2: Configure Phase 1 Factor Evolution

**Files:**
- Create: `rdagent/app/qlib_rd_loop/conf_phase1_factor_evolution.yaml`
- Modify: `rdagent/scenarios/qlib/baseline.py` (if needed for custom factors)

**Step 1: Review existing configuration**

```bash
# Check current Qlib scenario configuration
cat rdagent/app/qlib_rd_loop/conf.py | grep -A 20 "class.*Config"
```

Expected: Output shows existing configuration structure for `fin_factor` command

**Step 2: Create Phase 1 configuration file**

Write to `rdagent/app/qlib_rd_loop/conf_phase1_factor_evolution.yaml`:

```yaml
# Phase 1: Factor Evolution Configuration
# Fixed Model: LightGBM SOTA
# Objective: IC > 0.11

experiment:
  name: "phase1_factor_evolution"
  description: "Factor evolution with fixed LightGBM model"
  loop_n: 5  # 5 loops for Phase 1

# Starting factors (baseline)
start_factors:
  - name: "Price_Distance_Z_5D"
    formula: "(close - rolling_mean(close, 5)) / (rolling_std(close, 5) + 1e-8)"
    description: "5-day Z-score of price distance from mean"

  - name: "Price_Distance_Z_10D"
    formula: "(close - rolling_mean(close, 10)) / (rolling_std(close, 10) + 1e-8)"
    description: "10-day Z-score of price distance from mean"

  - name: "Price_Distance_Z_20D"
    formula: "(close - rolling_mean(close, 20)) / (rolling_std(close, 20) + 1e-8)"
    description: "20-day Z-score of price distance from mean"

# Model configuration (fixed for Phase 1)
model:
  type: "lightgbm"
  class: "LGBModel"
  module: "qlib.contrib.model.gbdt"

  # Loss function - prioritize IC but consider returns
  loss: "ic"

  # LightGBM hyperparameters
  loss_type: "all"
  colsample_bytree: 0.8879
  learning_rate: 0.0421
  subsample: 0.8789
  lambda_l1: 0.0
  lambda_l2: 0.0
  max_depth: 5
  num_leaves: 128
  num_threads: 20
  objective: "regression"
  seed: 123

# Factor evolution strategy
factor_evolution:
  # Directions to explore
  directions:
    - "multi_timeframe"  # Add 3D, 40D, 60D windows
    - "volume_combined"  # Combine Z-score with volume
    - "interaction_terms"  # Z_5D - Z_20D, etc.
    - "risk_adjusted"  # Z-score / volatility
    - "market_regime"  # Trend strength indicators

  # Constraints
  max_factors: 10
  min_ic: 0.05
  max_correlation: 0.7  # Between new and existing factors
  max_new_factors_per_loop: 2

# Data configuration
data:
  market: "cn_stock"
  freq: "day"
  train_period: ["2008-01-01", "2014-12-31"]
  valid_period: ["2015-01-01", "2016-12-31"]
  test_period: ["2017-01-01", "2020-12-31"]

# Evaluation metrics
evaluation:
  metrics:
    - "ic"
    - "rank_ic"
    - "annualized_return"
    - "max_drawdown"
    - "sharpe_ratio"

  target_values:
    ic: 0.11
    annualized_return: 0.0  # Neutral for Phase 1
    max_drawdown: 0.10

# Early stopping conditions
early_stop:
  trigger_after_loop: 3
  condition: "ic_improvement < 0.005"  # Less than 0.5% IC improvement
  action: "proceed_to_phase2"
```

**Step 3: Verify Qlib baseline models are available**

```bash
python -c "from qlib.contrib.model.gbdt import LGBModel; print('LGBModel available')" \
  || echo "Need to install qlib with models"
```

Expected: "LGBModel available"

If fails: Run `make init-qlib-env` from RD-Agent root

**Step 4: Test configuration file syntax**

```bash
python -c "import yaml; config = yaml.safe_load(open('rdagent/app/qlib_rd_loop/conf_phase1_factor_evolution.yaml')); print('Config valid:', 'experiment' in config)"
```

Expected: "Config valid: True"

**Step 5: Commit Phase 1 configuration**

```bash
git add rdagent/app/qlib_rd_loop/conf_phase1_factor_evolution.yaml
git commit -m "feat: add Phase 1 factor evolution configuration

- Configure 5-loop factor evolution with fixed LightGBM
- Define starting factors (Price_Distance_Z baseline)
- Set factor evolution directions and constraints
- Configure evaluation metrics and early stopping
"
```

---

## Task 3: Run Phase 1 Factor Evolution

**Files:**
- Create: `git_ignore_folder/experiment_tracking/run_phase1.sh`
- Modify: `docs/experiments/2026-01-23-co-optimization/real_time_log.md`

**Step 1: Create Phase 1 execution script**

Write to `git_ignore_folder/experiment_tracking/run_phase1.sh`:

```bash
#!/bin/bash
# Phase 1: Factor Evolution Execution
# Expected duration: ~50 minutes

set -e  # Exit on error

EXP_DIR="log/co-optimization-exp/phase1_factors"
LOG_FILE="docs/experiments/2026-01-23-co-optimization/real_time_log.md"
TRACK_SCRIPT="git_ignore_folder/experiment_tracking/track_experiment.sh"

echo "=========================================="
echo "Starting Phase 1: Factor Evolution"
echo "Time: $(date)"
echo "=========================================="

# Update real-time log
cat >> "$LOG_FILE" << EOF

## Phase 1 Execution Started
**Start Time**: $(date '+%Y-%m-%d %H:%M')
**Configuration**: rdagent/app/qlib_rd_loop/conf_phase1_factor_evolution.yaml
**Expected Duration**: ~50 minutes

**Plan**:
- Loop 1-2: Multi-timeframe expansion (3D, 40D, 60D)
- Loop 3-4: Volume combined factors
- Loop 5: Interaction terms (Z_diff, risk_adjusted)

EOF

# Activate conda environment
source ~/conda/etc/profile.d/conda.sh
conda activate quant

# Create experiment directory
mkdir -p "$EXP_DIR"

# Run Phase 1
echo "Starting factor evolution (5 loops)..."
rdagent fin_factor \
  --loop-n 5 \
  --target-dir "$EXP_DIR" \
  2>&1 | tee git_ignore_folder/experiment_tracking/phase1_output.log

echo "Phase 1 completed!"
echo "Experiment directory: $EXP_DIR"

# Extract and log results for each loop
for loop_num in {0..4}; do
  if [ -d "$EXP_DIR/Loop_$loop_num" ]; then
    echo "Extracting results for Loop $loop_num..."
    bash "$TRACK_SCRIPT" "$loop_num" "Phase1" "$EXP_DIR"
  fi
done

echo ""
echo "Phase 1 Summary:"
echo "================"
echo "Results logged to: $LOG_FILE"
echo "CSV summary: docs/experiments/2026-01-23-co-optimization/loop_summary.csv"
echo ""
echo "Next steps:"
echo "1. Review real_time_log.md for detailed results"
echo "2. Check if IC > 0.11 target achieved"
echo "3. If yes, proceed to Phase 2"
echo "4. If no, document findings and adjust strategy"
```

**Step 2: Make script executable**

```bash
chmod +x git_ignore_folder/experiment_tracking/run_phase1.sh
```

**Step 3: Pre-execution validation**

```bash
# Check environment
rdagent health_check

# Verify Qlib data
python -m qlib.cli.data get_data --target_dir ~/.qlib/qlib_data/cn_data --region cn --interval 1d --period 1day 2>&1 | grep -i "error" && echo "Data check failed" || echo "Data OK"

# Verify disk space (need ~5GB)
df -h . | tail -1 | awk '{if ($4+0 < 5) print "WARNING: Low disk space"; else print "Disk space OK"}'
```

Expected: All checks pass

**Step 4: Start Phase 1 execution**

```bash
# Option A: Interactive (to monitor in real-time)
bash git_ignore_folder/experiment_tracking/run_phase1.sh

# Option B: Background (recommended)
nohup bash git_ignore_folder/experiment_tracking/run_phase1.sh > git_ignore_folder/experiment_tracking/phase1_nohup.log 2>&1 &

# Record background process ID
echo $! > git_ignore_folder/experiment_tracking/phase1.pid

echo "Phase 1 running in background. Monitor with:"
echo "  tail -f git_ignore_folder/experiment_tracking/phase1_nohup.log"
echo "  tail -f git_ignore_folder/experiment_tracking/phase1_output.log"
```

**Step 5: Monitor Phase 1 progress**

While running, in a separate terminal:

```bash
# Check if process is still running
ps -p $(cat git_ignore_folder/experiment_tracking/phase1.pid) && echo "Running" || echo "Completed"

# View real-time logs
tail -f git_ignore_folder/experiment_tracking/phase1_output.log | grep -E "(Loop_|IC|Return|Completed)"

# Check experiment directory
watch -n 30 "ls -la log/co-optimization-exp/phase1_factors/ | grep Loop"
```

**Step 6: Wait for completion and verify results**

```bash
# Wait for process (if background)
wait $(cat git_ignore_folder/experiment_tracking/phase1.pid)

# Verify all 5 loops completed
ls -d log/co-optimization-exp/phase1_factors/Loop_* | wc -l
# Expected: 5

# Check final results
cat docs/experiments/2026-01-23-co-optimization/loop_summary.csv | tail -5
```

**Step 7: Generate Phase 1 summary report**

```bash
# Extract best loop
best_loop=$(awk -F',' 'NR>1 {print $1, $7}' docs/experiments/2026-01-23-co-optimization/loop_summary.csv | sort -k2 -rn | head -1 | awk '{print $1}')

echo "Best Loop in Phase 1: Loop_$best_loop"

# View detailed feedback
cat log/co-optimization-exp/phase1_factors/Loop_$best_loop/feedback/*.txt
```

**Step 8: Update decision log**

Manually append to `docs/experiments/2026-01-23-co-optimization/decision_log.md`:

```markdown
## Decision 1: Phase 1 Completion Assessment

**Time**: [After Phase 1 completion]
**Context**: Phase 1 completed 5 loops of factor evolution

**Results**:
- Best IC: [Fill from results]
- Best Loop: Loop_[number]
- Factors used: [List best factors]

**Options**:
- A: Proceed to Phase 2 if IC > 0.105
- B: Extend Phase 1 for 2 more loops if IC 0.102-0.105
- C: Re-strategize if IC < 0.102

**Selection**: [To be decided based on results]
**Rationale**: [To be filled]
```

**Step 9: Commit Phase 1 execution scripts and results**

```bash
git add git_ignore_folder/experiment_tracking/run_phase1.sh
git add docs/experiments/2026-01-23-co-optimization/
git add log/co-optimization-exp/phase1_factors/
git commit -m "exp: Phase 1 factor evolution completed

- Ran 5 loops of factor evolution with fixed LightGBM
- Achieved IC: [value] (target: > 0.11)
- Best factors: [list]
- Results tracked in experiment documentation
"
```

---

## Task 4: Configure Phase 2 Model Optimization

**Files:**
- Create: `rdagent/app/qlib_rd_loop/conf_phase2_model_optimization.yaml`
- Modify: `docs/experiments/2026-01-23-co-optimization/real_time_log.md`

**Step 1: Identify best factors from Phase 1**

```bash
# Get best loop from Phase 1
best_loop=$(awk -F',' 'NR>1 {print $1, $7}' docs/experiments/2026-01-23-co-optimization/loop_summary.csv | sort -k2 -rn | head -1 | awk '{print $1}')

# Extract factor definitions
python << 'EOF'
import yaml
import glob

# Find best loop config
config_files = glob.glob(f"log/co-optimization-exp/phase1_factors/Loop_{best_loop}/task_*/experiment_config.yaml")
if config_files:
    with open(config_files[0]) as f:
        config = yaml.safe_load(f)
        factors = config.get('factors', [])
        print("Best factors from Phase 1:")
        for factor in factors:
            print(f"  - {factor.get('name')}: {factor.get('formula')}")
EOF
```

Expected: List of best factors with formulas

**Step 2: Create Phase 2 configuration**

Write to `rdagent/app/qlib_rd_loop/conf_phase2_model_optimization.yaml`:

```yaml
# Phase 2: Model Optimization Configuration
# Fixed Factors: [Best from Phase 1]
# Objective: Annual returns > 5%

experiment:
  name: "phase2_model_optimization"
  description: "Model optimization with fixed best factors from Phase 1"
  loop_n: 5  # 5 loops for Phase 2

# Fixed factors (from Phase 1 best)
# TO BE FILLED after Phase 1 completes
fixed_factors:
  - name: "Price_Distance_Z_5D"
    formula: "(close - rolling_mean(close, 5)) / (rolling_std(close, 5) + 1e-8)"

  # Add other best factors from Phase 1 here

# Model candidates to explore
model_candidates:
  - name: "lightgbm_v1"
    type: "lightgbm"
    class: "LGBModel"
    description: "LightGBM with optimized loss for returns"
    config:
      loss: "ic_with_return_penalty"  # Custom loss balancing IC and returns
      learning_rate: 0.03
      num_leaves: 63
      max_depth: 7
      colsample_bytree: 0.8
      subsample: 0.8
      lambda_l1: 0.1  # Add regularization
      lambda_l2: 0.1

  - name: "lightgbm_v2"
    type: "lightgbm"
    class: "LGBModel"
    description: "LightGBM with higher regularization"
    config:
      loss: "ic"
      learning_rate: 0.02
      num_leaves: 31
      max_depth: 5
      colsample_bytree: 0.7
      subsample: 0.7
      lambda_l1: 1.0  # Strong regularization
      lambda_l2: 1.0

  - name: "mlp_v1"
    type: "mlp"
    class: "MLP"
    description: "3-layer MLP for nonlinear interactions"
    config:
      hidden_layers: [128, 64, 32]
      activation: "relu"
      dropout: 0.3
      learning_rate: 0.001
      batch_size: 2048
      epochs: 100
      early_stopping_patience: 10

  - name: "hist_v1"
    type: "hist"
    class: "HIST"
    description: "Histogram-based gradient boosting"
    config:
      loss: "ic"
      learning_rate: 0.05
      max_leaf_nodes: 63
      max_depth: 7

# Model evolution strategy
model_evolution:
  # Priority order for model selection
  priority: ["lightgbm_v1", "lightgbm_v2", "mlp_v1", "hist_v1"]

  # Hyperparameter optimization
  hyperparameter_optimization:
    method: "grid_search"  # Options: grid_search, random_search, bayesian
    n_trials: 3

  # Multi-objective optimization
  objectives:
    primary: "annualized_return"
    secondary: "ic"
    constraints:
      max_drawdown: 0.10
      min_ic: 0.10

# Loss function modifications
loss_functions:
  ic_with_return_penalty:
    formula: "IC - alpha * max(0, -return)"
    alpha: 0.5  # Penalty weight for negative returns

  sharpe_optimized:
    formula: "return / volatility"
    target: "maximize"

# Data configuration (same as Phase 1)
data:
  market: "cn_stock"
  freq: "day"
  train_period: ["2008-01-01", "2014-12-31"]
  valid_period: ["2015-01-01", "2016-12-31"]
  test_period: ["2017-01-01", "2020-12-31"]

# Evaluation metrics
evaluation:
  metrics:
    - "ic"
    - "annualized_return"
    - "max_drawdown"
    - "sharpe_ratio"

  target_values:
    ic: 0.10  # Slightly relaxed to allow returns focus
    annualized_return: 0.05  # Primary target
    max_drawdown: 0.10

  # Validation set monitoring
  validation_monitoring:
    metric: "annualized_return"
    patience: 3
    min_improvement: 0.01  # 1% improvement

# Early stopping conditions
early_stop:
  trigger_after_loop: 3
  condition: "return_improvement < 0.01 and drawdown > 0.12"
  action: "review_and_adjust"
```

**Step 3: Update Phase 2 configuration with actual best factors**

```bash
# Extract actual best factors and update config
# (This will be done manually after Phase 1 completes)
```

**Step 4: Commit Phase 2 configuration**

```bash
git add rdagent/app/qlib_rd_loop/conf_phase2_model_optimization.yaml
git commit -m "feat: add Phase 2 model optimization configuration

- Configure 5-loop model optimization with fixed best factors
- Define model candidates (LightGBM variants, MLP, HIST)
- Set up multi-objective optimization (returns primary, IC secondary)
- Configure loss function modifications to penalize negative returns
- Note: Fixed factors section to be filled after Phase 1 completion
"
```

---

## Task 5: Run Phase 2 Model Optimization

**Files:**
- Create: `git_ignore_folder/experiment_tracking/run_phase2.sh`
- Modify: `docs/experiments/2026-01-23-co-optimization/real_time_log.md`

**Step 1: Create Phase 2 execution script**

Write to `git_ignore_folder/experiment_tracking/run_phase2.sh`:

```bash
#!/bin/bash
# Phase 2: Model Optimization Execution
# Expected duration: ~40 minutes
# PREREQUISITE: Phase 1 must be completed

set -e

EXP_DIR="log/co-optimization-exp/phase2_models"
LOG_FILE="docs/experiments/2026-01-23-co-optimization/real_time_log.md"
TRACK_SCRIPT="git_ignore_folder/experiment_tracking/track_experiment.sh"
PHASE1_DIR="log/co-optimization-exp/phase1_factors"

echo "=========================================="
echo "Starting Phase 2: Model Optimization"
echo "Time: $(date)"
echo "=========================================="

# Check Phase 1 completion
if [ ! -d "$PHASE1_DIR" ]; then
  echo "ERROR: Phase 1 directory not found. Run Phase 1 first."
  exit 1
fi

# Update real-time log
cat >> "$LOG_FILE" << EOF

## Phase 2 Execution Started
**Start Time**: $(date '+%Y-%m-%d %H:%M')
**Configuration**: rdagent/app/qlib_rd_loop/conf_phase2_model_optimization.yaml
**Expected Duration**: ~40 minutes

**Fixed Factors**: [Extracted from Phase 1 best]

**Model Candidates**:
- Loop 6: LightGBM v1 (return-optimized loss)
- Loop 7: LightGBM v2 (high regularization)
- Loop 8: MLP v1 (nonlinear)
- Loop 9: HIST v1 (histogram-based)
- Loop 10: Best model fine-tuning

EOF

# Activate conda environment
source ~/conda/etc/profile.d/conda.sh
conda activate quant

# Create experiment directory
mkdir -p "$EXP_DIR"

# Get Phase 1 best loop
best_phase1_loop=$(awk -F',' 'NR>1 {print $1, $7}' docs/experiments/2026-01-23-co-optimization/loop_summary.csv | grep "Phase1" | sort -k2 -rn | head -1 | awk '{print $1}')

echo "Using best factors from Phase 1 Loop_$best_phase1_loop"

# Run Phase 2 (model evolution)
echo "Starting model optimization (5 loops)..."
rdagent fin_model \
  --loop-n 5 \
  --target-dir "$EXP_DIR" \
  2>&1 | tee git_ignore_folder/experiment_tracking/phase2_output.log

echo "Phase 2 completed!"
echo "Experiment directory: $EXP_DIR"

# Extract and log results
for loop_num in {0..4}; do
  if [ -d "$EXP_DIR/Loop_$loop_num" ]; then
    echo "Extracting results for Loop $loop_num..."
    bash "$TRACK_SCRIPT" "$((loop_num + 6))" "Phase2" "$EXP_DIR"
  fi
done

echo ""
echo "Phase 2 Summary:"
echo "================"
echo "Results logged to: $LOG_FILE"
echo ""
echo "Key questions:"
echo "1. Did any model achieve returns > 0%?"
echo "2. Which model has best Sharpe ratio?"
echo "3. Is IC maintained above 0.10?"
```

**Step 2: Make executable and run**

```bash
chmod +x git_ignore_folder/experiment_tracking/run_phase2.sh

# Run in background
nohup bash git_ignore_folder/experiment_tracking/run_phase2.sh > git_ignore_folder/experiment_tracking/phase2_nohup.log 2>&1 &

echo $! > git_ignore_folder/experiment_tracking/phase2.pid
```

**Step 3: Monitor Phase 2**

Similar to Task 3, Step 5-7

**Step 4: Commit Phase 2 results**

```bash
git add git_ignore_folder/experiment_tracking/run_phase2.sh
git add docs/experiments/2026-01-23-co-optimization/
git add log/co-optimization-exp/phase2_models/
git commit -m "exp: Phase 2 model optimization completed

- Ran 5 loops of model optimization with fixed best factors
- Tested models: [list tested models]
- Best model: [name] with returns: [value]
- Results tracked in experiment documentation
"
```

---

## Task 6: Configure and Run Phase 3 Joint Fine-tuning

**Files:**
- Create: `rdagent/app/qlib_rd_loop/conf_phase3_joint_tuning.yaml`
- Create: `git_ignore_folder/experiment_tracking/run_phase3.sh`

**Step 1: Create Phase 3 configuration**

Write to `rdagent/app/qlib_rd_loop/conf_phase3_joint_tuning.yaml`:

```yaml
# Phase 3: Joint Fine-tuning
# Optimize factor weights + model hyperparameters together

experiment:
  name: "phase3_joint_tuning"
  description: "Joint optimization of factor weights and model parameters"
  loop_n: 5

# Joint optimization strategy
joint_optimization:
  method: "sequential"  # Options: sequential, simultaneous, ensemble

  # Loop 11: Factor weight optimization
  loop_11:
    focus: "factor_weights"
    method: "genetic_algorithm"
    fixed_model: "[Best model from Phase 2]"
    optimization_target: "sharpe_ratio"

  # Loop 12-13: Model ensemble
  loop_12_13:
    focus: "model_ensemble"
    candidates:
      - "[Best model from Phase 2]"
      - "Second best model from Phase 2"
    ensemble_methods:
      - "soft_voting"  # Weighted average
      - "stacking"     # Meta-learner

  # Loop 14: Transaction cost optimization
  loop_14:
    focus: "trading_costs"
    strategies:
      - "signal_thresholding"  # Only trade on strong signals
      - "position_sizing"      # Scale positions by signal strength
    thresholds: [0.01, 0.02, 0.05]

  # Loop 15: Final integration
  loop_15:
    focus: "final_integration"
    apply:
      - "best_factor_weights"
      - "best_ensemble"
      - "best_threshold"
    evaluate_all_metrics: true

# Factor weight optimization
factor_weight_optimization:
  constraints:
    sum_weights: 1.0
    min_weight: 0.0  # No shorting factors
    max_weight: 0.5  # No single factor dominates

  optimization_objective:
    maximize: "sharpe_ratio"
    subject_to:
      ic: ">= 0.10"
      max_drawdown: "<= 0.10"

# Model ensemble configuration
model_ensemble:
  soft_voting:
    weight_search: "grid"
    weight_combinations:
      - [1.0, 0.0]  # Single model
      - [0.7, 0.3]  # Primary + secondary
      - [0.5, 0.5]  # Equal

  stacking:
    meta_model: "linear_regression"
    features: ["model1_prediction", "model2_prediction", "ic_model1", "ic_model2"]

# Trading cost optimization
trading_cost_optimization:
  signal_thresholding:
    metric: "prediction_change"
    thresholds:
      - 0.01  # Trade on 1% change
      - 0.02  # Trade on 2% change
      - 0.05  # Trade on 5% change
    objective: "maximize_return_after_costs"

  position_sizing:
    method: "sigmoid"
    formula: "position = sigmoid(alpha * prediction) * risk_adjustment"
    alpha_options: [1, 2, 5]

# Evaluation criteria (all must be met)
evaluation:
  success_criteria:
    ic: "> 0.11"
    annualized_return: "> 0.05"
    max_drawdown: "< 0.10"
    cross_period_stability: "all_years_profitable"

  pareto_analysis:
    objectives: ["ic", "annualized_return", "-max_drawdown"]
    select_from_pareto_front: "most_balanced"
```

**Step 2: Create Phase 3 execution script**

Write to `git_ignore_folder/experiment_tracking/run_phase3.sh`:

```bash
#!/bin/bash
# Phase 3: Joint Fine-tuning Execution
# Expected duration: ~40 minutes

set -e

EXP_DIR="log/co-optimization-exp/phase3_joint"
LOG_FILE="docs/experiments/2026-01-23-co-optimization/real_time_log.md"

echo "=========================================="
echo "Starting Phase 3: Joint Fine-tuning"
echo "Time: $(date)"
echo "=========================================="

cat >> "$LOG_FILE" << EOF

## Phase 3 Execution Started
**Start Time**: $(date '+%Y-%m-%d %H:%M')
**Expected Duration**: ~40 minutes

**Plan**:
- Loop 11: Factor weight optimization (genetic algorithm)
- Loop 12-13: Model ensemble testing
- Loop 14: Transaction cost optimization
- Loop 15: Final integration and evaluation

EOF

source ~/conda/etc/profile.d/conda.sh
conda activate quant

mkdir -p "$EXP_DIR"

# Run full co-optimization
echo "Starting joint fine-tuning (5 loops)..."
rdagent fin_quant \
  --loop-n 5 \
  --target-dir "$EXP_DIR" \
  2>&1 | tee git_ignore_folder/experiment_tracking/phase3_output.log

echo "Phase 3 completed!"

# Log results
for loop_num in {0..4}; do
  bash git_ignore_folder/experiment_tracking/track_experiment.sh "$((loop_num + 11))" "Phase3" "$EXP_DIR"
done

echo "Check if all targets achieved:"
cat docs/experiments/2026-01-23-co-optimization/loop_summary.csv | tail -5
```

**Step 3: Execute Phase 3**

```bash
chmod +x git_ignore_folder/experiment_tracking/run_phase3.sh

nohup bash git_ignore_folder/experiment_tracking/run_phase3.sh > git_ignore_folder/experiment_tracking/phase3_nohup.log 2>&1 &

echo $! > git_ignore_folder/experiment_tracking/phase3.pid
```

**Step 4: Commit Phase 3 setup and results**

```bash
git add rdagent/app/qlib_rd_loop/conf_phase3_joint_tuning.yaml
git add git_ignore_folder/experiment_tracking/run_phase3.sh
git add log/co-optimization-exp/phase3_joint/
git commit -m "exp: Phase 3 joint fine-tuning completed

- Optimized factor weights using genetic algorithm
- Tested model ensemble strategies
- Applied transaction cost optimization
- Final integration and evaluation
- Overall results: [summary]
"
```

---

## Task 7: Generate Final Report and Lessons Learned

**Files:**
- Create: `docs/experiments/2026-01-23-co-optimization/final_report.md`
- Modify: `docs/experiments/2026-01-23-co-optimization/lessons_learned.md`

**Step 1: Extract all results**

```bash
# Generate summary statistics
python << 'EOF'
import pandas as pd
import glob

# Read loop summary
df = pd.read_csv('docs/experiments/2026-01-23-co-optimization/loop_summary.csv')

print("=== Experiment Summary ===")
print(f"Total Loops: {len(df)}")
print(f"Phases: {df['Phase'].unique()}")
print()
print("Best IC:", df['IC'].max())
print("Best Returns:", df['Ann_Return'].str.rstrip('%').astype(float).max(), "%")
print("Lowest Drawdown:", df['Max_Drawdown'].str.rstrip('%').astype(float).min(), "%")

# Find best overall loop
df['returns_numeric'] = df['Ann_Return'].str.rstrip('%').astype(float)
df['ic_numeric'] = df['IC'].astype(float)

# Composite score: IC + Returns (if positive)
df['composite_score'] = df['ic_numeric'] + df['returns_numeric'].apply(lambda x: max(0, x/10))

best_loop = df.loc[df['composite_score'].idxmax()]
print()
print("Best Overall Loop:", best_loop['Loop'])
print("  Phase:", best_loop['Phase'])
print("  IC:", best_loop['IC'])
print("  Returns:", best_loop['Ann_Return'])
print("  Drawdown:", best_loop['Max_Drawdown'])
EOF
```

**Step 2: Generate final report**

Write to `docs/experiments/2026-01-23-co-optimization/final_report.md`:

```markdown
# Factor-Model Co-optimization Final Report

**Experiment Date**: 2026-01-23
**Total Duration**: [Calculate from timestamps]
**Total Loops**: 15

---

## Executive Summary

### Goal Achievement

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| IC | > 0.11 | [value] | [✅/❌] |
| Annual Returns | > 5% | [value]% | [✅/❌] |
| Max Drawdown | < 10% | [value]% | [✅/❌] |
| Cross-period Stability | All profitable | [status] | [✅/❌] |

### Best Solution

**Factors**: [List with weights]
**Model**: [Name and config]
**Performance**:
- IC: [value]
- Returns: [value]%
- Drawdown: [value]%
- Sharpe: [value]

---

## Phase-by-Phase Results

### Phase 1: Factor Evolution (Loop 1-5)

**Objective**: IC > 0.11 with fixed LightGBM
**Duration**: [time]

**Results**:
- Starting IC: 0.102
- Best IC: [value] (Loop [X])
- IC Improvement: [value]%
- Best Factors: [list]

**Key Findings**:
1. [Finding 1]
2. [Finding 2]

**Successful Strategies**:
- [What worked]

**Failed Attempts**:
- [What didn't work and why]

---

### Phase 2: Model Optimization (Loop 6-10)

**Objective**: Returns > 5% with fixed best factors
**Duration**: [time]

**Results**:
- Starting Returns: [Phase1 result]%
- Best Returns: [value]% (Loop [X])
- Best Model: [name]

**Model Comparison**:

| Model | IC | Returns | Drawdown | Sharpe |
|-------|-----|---------|----------|--------|
| LightGBM v1 | [val] | [val]% | [val]% | [val] |
| LightGBM v2 | [val] | [val]% | [val]% | [val] |
| MLP v1 | [val] | [val]% | [val]% | [val] |
| HIST v1 | [val] | [val]% | [val]% | [val] |

**Key Findings**:
1. [Which model worked best and why]
2. [Hyperparameter sensitivity]
3. [IC vs Returns trade-off]

---

### Phase 3: Joint Fine-tuning (Loop 11-15)

**Objective**: Balance all metrics
**Duration**: [time]

**Results**:
- Loop 11 (Factor Weights): [results]
- Loop 12-13 (Ensemble): [results]
- Loop 14 (Cost Optimization): [results]
- Loop 15 (Final): [results]

**Optimization Effectiveness**:

| Aspect | Before Phase 3 | After Phase 3 | Change |
|--------|----------------|---------------|--------|
| IC | [val] | [val] | [Δ]% |
| Returns | [val]% | [val]% | [Δ]% |
| Drawdown | [val]% | [val]% | [Δ]% |

**Key Findings**:
1. [Impact of factor weight optimization]
2. [Ensemble vs single model]
3. [Trading cost optimization impact]

---

## Key Insights

### Factor Design

**What Worked**:
1. [Strategy 1] - [why it worked]
2. [Strategy 2] - [why it worked]

**What Didn't Work**:
1. [Strategy 1] - [why it failed]
2. [Strategy 2] - [why it failed]

**Critical Insight**:
[Most important learning about factors]

### Model Selection

**Best Model**: [name]
**Reason**: [explanation]

**Model Hierarchy**:
1. [Best for IC]
2. [Best for Returns]
3. [Best for Risk Control]

### Interaction Effects

**How Factors and Models Interact**:
[Discussion of interesting interactions]

**Example**:
[Specific case where factor-model combination was unexpected]

---

## Pareto Front Analysis

[A discussion of trade-offs between different objectives]

[If possible, include visual representation of Pareto front]

**Selected Solution**: [Why this particular point on the front was chosen]

---

## Cross-Period Stability

### Yearly Breakdown

| Year | IC | Returns | Drawdown | Profitable? |
|------|-----|---------|----------|-------------|
| 2017 | [val] | [val]% | [val]% | [✅/❌] |
| 2018 | [val] | [val]% | [val]% | [✅/❌] |
| 2019 | [val] | [val]% | [val]% | [✅/❌] |
| 2020 | [val] | [val]% | [val]% | [✅/❌] |

**Stability Analysis**:
[Discussion of consistency across years]

---

## Failure Analysis

### Failed Attempts

Total failed strategies: [count]

1. **[Failed Strategy 1]**
   - **Hypothesis**: [What was expected]
   - **Result**: [What actually happened]
   - **Reason**: [Why it failed]
   - **Learning**: [What this teaches us]

2. **[Failed Strategy 2]**
   - [...]

[Continue for all major failures]

---

## Conclusions

### Did We Achieve Our Goals?

**Overall**: [Yes/No/Partially]

**Detailed Assessment**:
- IC: [assessment]
- Returns: [assessment]
- Risk: [assessment]
- Stability: [assessment]

### Success Factors

1. [Factor 1]
2. [Factor 2]
3. [Factor 3]

### Limitations

1. [Limitation 1]
2. [Limitation 2]
3. [Limitation 3]

---

## Recommendations for Next Steps

### If Goals Were Met

**Further Optimization**:
1. [Direction 1]
2. [Direction 2]

**Production Deployment**:
1. [Deployment consideration 1]
2. [Deployment consideration 2]

### If Goals Were Not Met

**Alternative Approaches**:
1. [Alternative 1] - [why]
2. [Alternative 2] - [why]

**What to Try Differently**:
1. [Different approach 1]
2. [Different approach 2]

---

## Appendices

### A. Complete Loop-by-Loop Results
[Attach full CSV or table]

### B. Factor Formulas
[Complete mathematical formulas for all factors]

### C. Model Configurations
[Full model hyperparameters]

### D. Experiment Logs
[Link to real_time_log.md]

---

*Report Generated: 2026-01-23*
*Experiment ID: co-optimization-2026-01-23*
```

**Step 3: Generate lessons learned**

Write to `docs/experiments/2026-01-23-co-optimization/lessons_learned.md`:

```markdown
# Lessons Learned - Factor-Model Co-optimization

**Experiment**: 2026-01-23 Co-optimization
**Summary**: [Brief summary of outcomes]

---

## 1. Factor Design Lessons

### ✅ Proven Effective

#### Z-Score Normalization
**Insight**: Standardizing factors by their own volatility significantly improves IC
**Evidence**: IC improved from [baseline] to [value]
**Reason**: Eliminates scale differences between stocks
**Future Use**: Apply Z-score normalization as default for all price-based factors

#### Multi-Timeframe Combinations
**Insight**: Combining 5D, 10D, 20D windows outperforms single windows
**Evidence**: [data]
**Reason**: Captures both short-term momentum and long-term trends
**Future Use**: Always test multiple timeframes

#### Volume-Price Interaction
**Insight**: Volume-adjusted factors provide incremental information
**Evidence**: VPT and OBV factors showed positive IC
**Reason**: Volume confirms price movements
**Future Use**: Consider volume information for price factors

### ❌ Proven Ineffective

#### Excessive Time Windows
**Insight**: Windows > 60 days introduce lag
**Evidence**: IC decreased when using 60D, 120D windows
**Reason**: Long windows adapt too slowly to market changes
**Future Avoid**: Limit windows to ≤ 40 days for daily data

#### Raw Price Values
**Insight**: Unnormalized price factors underperform
**Evidence**: [comparison data]
**Reason**: Different stocks have different price scales
**Future Avoid**: Always normalize or standardize

### 💡 Critical Insights

1. **IC ≠ Returns**: High IC doesn't guarantee positive returns
   - **Reason**: IC measures correlation, not profitability after costs
   - **Solution**: Optimize for Sharpe ratio, not just IC

2. **Statistical Standardization is Key**:
   - **Finding**: Z-score consistently outperforms raw values
   - **Implication**: Make normalization a standard preprocessing step

3. **Factor Interaction Matters**:
   - **Finding**: Some factors work well together, others don't
   - **Implication**: Test factor combinations, not just individual factors

---

## 2. Model Selection Lessons

### ✅ Model Performance Ranking

1. **[Best Model]**
   - **Best for**: [use case]
   - **Why**: [reason]
   - **When to use**: [conditions]

2. **[Second Best]**
   - **Best for**: [use case]
   - **Why**: [reason]
   - **When to use**: [conditions]

3. **[Third Best]**
   - [...]

### Model Selection Guidelines

| Situation | Recommended Model | Reason |
|-----------|------------------|--------|
| High IC priority | [model] | [reason] |
| Returns priority | [model] | [reason] |
| Limited compute | [model] | [reason] |
| Many factors | [model] | [reason] |

### Hyperparameter Sensitivity

**Learning Rate**:
- **Finding**: Lower LR → better generalization but slower training
- **Sweet spot**: [value]
- **Rule of thumb**: Start with 0.03-0.05

**Regularization**:
- **Finding**: L1/L2 regularization crucial for preventing overfitting
- **Sweet spot**: λ = 0.1-1.0
- **Trade-off**: Too much regularization hurts IC

**Tree Depth / Network Size**:
- **Finding**: Deeper trees/networks don't always help
- **Sweet spot**: [specific values]
- **Risk**: Overfitting on training data

### Loss Function Design

**Standard IC Loss**:
- **Pros**: Maximizes prediction correlation
- **Cons**: Doesn't consider transaction costs or risk
- **Use when**: Pure prediction accuracy is goal

**Custom Return-Weighted Loss**:
- **Pros**: Directly optimizes for returns
- **Cons**: May sacrifice IC
- **Use when**: Profitability is primary goal

**Sharpe-Optimized Loss**:
- **Pros**: Balances return and risk
- **Cons**: Complex to implement
- **Use when**: Risk-adjusted returns matter

---

## 3. Co-optimization Strategy Lessons

### Iterative Approach (What We Did)

**Advantages**:
- Computationally efficient (2-3 hours)
- Easy to debug and trace issues
- Each component fully optimized

**Disadvantages**:
- May miss factor-model specific combinations
- Order-dependent (factor-first vs model-first matters)

**When to Use**: [guidance]

### What We Should Try Next Time

1. **Synchronized Co-optimization**
   - **Why**: May discover better factor-model pairings
   - **Cost**: 2x computation time
   - **Try when**: Have ample compute time

2. **Factor Orthogonalization**
   - **Why**: Reduce redundancy between factors
   - **Method**: PCA or Gram-Schmidt on factor matrix
   - **Expected benefit**: More robust model

3. **Market Regime Detection**
   - **Why**: Different factors work in different markets
   - **Method**: Cluster market states, use regime-specific models
   - **Expected benefit**: Improved cross-period stability

---

## 4. Experimental Workflow Lessons

### What Worked Well

1. **Automated Tracking Scripts**
   - **Benefit**: Real-time logging without manual effort
   - **Implementation**: `track_experiment.sh`
   - **ROI**: High - saved hours of manual work

2. **Phase-wise Approach**
   - **Benefit**: Clear progress milestones
   - **Implementation**: 3 phases with checkpoints
   - **ROI**: High - enabled early course correction

3. **Comprehensive Documentation**
   - **Benefit**: Easy to review and understand decisions
   - **Implementation**: Multiple markdown files
   - **ROI**: High - valuable for future reference

### What Didn't Work Well

1. **[Issue 1]**
   - **Problem**: [description]
   - **Impact**: [consequence]
   - **Fix for next time**: [solution]

2. **[Issue 2]**
   - **Problem**: [description]
   - **Impact**: [consequence]
   - **Fix for next time**: [solution]

### Process Improvements for Next Time

**Before Experiment**:
- [Improvement 1]
- [Improvement 2]

**During Experiment**:
- [Improvement 1]
- [Improvement 2]

**After Experiment**:
- [Improvement 1]
- [Improvement 2]

---

## 5. Technical Insights

### RD-Agent Framework

**Strengths**:
- [Strength 1]
- [Strength 2]

**Weaknesses**:
- [Weakness 1]
- [Weakness 2]

**Tips for Efficient Use**:
1. [Tip 1]
2. [Tip 2]

### Qlib Platform

**Strengths**:
- [Strength 1]
- [Strength 2]

**Weaknesses**:
- [Weakness 1]
- [Weakness 2]

**Tips for Efficient Use**:
1. [Tip 1]
2. [Tip 2]

### Computation Optimization

**Time Breakdown**:
- Phase 1: [time] ([percent]%)
- Phase 2: [time] ([percent]%)
- Phase 3: [time] ([percent]%)
- Evaluation: [time] ([percent]%)

**Bottlenecks**:
1. [Bottleneck 1]
2. [Bottleneck 2]

**Optimization Opportunities**:
1. [Opportunity 1]
2. [Opportunity 2]

---

## 6. Domain Knowledge (Quant Finance)

### Factor Categories

**Momentum Factors**:
- **What works**: [specific type]
- **What doesn't**: [specific type]
- **Why**: [explanation]

**Reversion Factors**:
- **What works**: [specific type]
- **What doesn't**: [specific type]
- **Why**: [explanation]

**Volume Factors**:
- **What works**: [specific type]
- **What doesn't**: [specific type]
- **Why**: [explanation]

### Market Regimes

**Trending Markets**:
- **Best factors**: [list]
- **Best models**: [list]
- **Characteristics**: [description]

**Range-Bound Markets**:
- **Best factors**: [list]
- **Best models**: [list]
- **Characteristics**: [description]

**Volatile Markets**:
- **Best factors**: [list]
- **Best models**: [list]
- **Characteristics**: [description]

### Risk Management

**Drawdown Control**:
- **Effective strategies**: [list]
- **Ineffective strategies**: [list]

**Position Sizing**:
- **What we learned**: [insights]
- **Recommendations**: [guidance]

---

## 7. Future Research Directions

### Short-term Experiments (Next 1-2 weeks)

1. **[Experiment 1]**
   - **Hypothesis**: [what we expect]
   - **Method**: [how to test]
   - **Expected outcome**: [prediction]

2. **[Experiment 2]**
   - [...]

### Medium-term Explorations (Next 1-2 months)

1. **[Exploration 1]**
   - **Rationale**: [why it's promising]
   - **Requirements**: [what's needed]
   - **Success criteria**: [how to evaluate]

2. **[Exploration 2]**
   - [...]

### Long-term Research (Next 3-6 months)

1. **[Research Direction 1]**
   - **Potential impact**: [what it could achieve]
   - **Feasibility**: [how realistic]
   - **Resources needed**: [what's required]

2. **[Research Direction 2]**
   - [...]

---

## 8. Advice for Future Experiments

### Do's

1. **Start Simple**: Begin with proven factors, then iterate
2. **Document Everything**: Real-time logging saves time later
3. **Use Checkpoints**: Evaluate after each phase
4. **Monitor Overfitting**: Validate on out-of-sample data
5. **Consider Trading Costs**: High IC doesn't mean profitable

### Don'ts

1. **Don't Over-Optimize**: More factors ≠ better results
2. **Don't Ignore Risk**: Returns without drawdown control are dangerous
3. **Don't Trust Single Metrics**: IC, returns, and Sharpe all matter
4. **Don't Skip Cross-Validation**: In-sample performance lies
5. **Don't Forget Transaction Costs**: Real trading has frictions

### Rules of Thumb

- **Factor count**: Keep < 10 for stability
- **Time windows**: Use 5-40 day range for daily data
- **Model complexity**: Simple models often generalize better
- **Evaluation**: Always use walk-forward validation
- **Success criteria**: Target IC > 0.10, returns > 5%, drawdown < 10%

---

## 9. Top 10 Takeaways

1. **Z-score normalization is the single most effective technique** - consistently improves IC across all factor types

2. **IC ≠ profitability** - high correlation doesn't guarantee profits after costs

3. **Multi-timeframe factors outperform single windows** - 5D/10D/20D combination is robust

4. **Volume information adds value** - VPT and OBV provide incremental signals

5. **Regularization is critical** - prevents overfitting and improves out-of-sample performance

6. **Factor interactions matter** - test combinations, not just individual factors

7. **Model choice impacts objectives** - LightGBM for IC, custom loss for returns

8. **Market regime awareness helps** - different factors work in different conditions

9. **Automated tracking is essential** - saves time and enables better analysis

10. **Iterative optimization works** - phase-wise approach balances efficiency and effectiveness

---

*Last Updated: 2026-01-23*
*This document will be updated as we conduct more experiments*
```

**Step 4: Commit all documentation**

```bash
git add docs/experiments/2026-01-23-co-optimization/
git commit -m "docs: add final report and lessons learned for co-optimization experiment

- Comprehensive final report with phase-by-phase analysis
- Detailed lessons learned covering factors, models, and workflow
- Actionable insights for future experiments
- Top 10 key takeaways summarized
"
```

---

## Task 8: Cleanup and Archive

**Files:**
- Create: `docs/experiments/2026-01-23-co-optimization/README_ARCHIVE.md`

**Step 1: Archive experiment logs**

```bash
# Compress large log files
tar -czf git_ignore_folder/experiment_logs_2026-01-23.tar.gz \
  log/co-optimization-exp/ \
  git_ignore_folder/experiment_tracking/*.log

# Remove uncompressed logs to save space
# rm -rf log/co-optimization-exp/  # Uncomment if space is critical
# rm git_ignore_folder/experiment_tracking/*.log  # Uncomment if space is critical
```

**Step 2: Create archive README**

Write to `docs/experiments/2026-01-23-co-optimization/README_ARCHIVE.md`:

```markdown
# Experiment Archive

**Experiment ID**: co-optimization-2026-01-23
**Date**: 2026-01-23
**Status**: [Completed/Running]

## Archived Files

- `experiment_logs_2026-01-23.tar.gz` - Complete experiment logs
- `loop_summary.csv` - Quantitative results summary
- `final_report.md` - Comprehensive analysis
- `lessons_learned.md` - Key insights

## How to Extract

```bash
tar -xzf git_ignore_folder/experiment_logs_2026-01-23.tar.gz
```

## Key Results Summary

[Add quick summary table]
```

**Step 3: Final commit**

```bash
git add docs/experiments/2026-01-23-co-optimization/README_ARCHIVE.md
git commit -m "docs: archive co-optimization experiment

- Compressed experiment logs
- Created archive README
- Quick summary documented
"
```

---

## Success Criteria

The implementation is complete when:

1. ✅ All 8 tasks completed without errors
2. ✅ 15 loops of co-optimization executed successfully
3. ✅ Results documented in final_report.md
4. ✅ Lessons captured in lessons_learned.md
5. ✅ Git repository contains complete history
6. ✅ Archive created for long-term storage

---

## Notes for Execution

- **Total estimated time**: 2-3 hours (mostly automated waiting)
- **Monitoring required**: Check progress every 20-30 minutes
- **Key checkpoints**: After Phase 1, Phase 2, Phase 3
- **Decision points**: Whether to proceed or adjust strategy
- **Documentation**: Update logs in real-time for best results

---

*End of Implementation Plan*
