# Factor-Model Co-optimization Real-time Log

**Experiment ID**: co-optimization-2026-01-23
**Start Time**: 2026-01-23 [Starting now]
**Target**: IC > 0.11, Returns > 5%, Drawdown < 10%, Stable across 2017-2020

---

## Experiment Initialization

**Time**: 2026-01-23 [In Progress]
**Action**: Setting up experiment infrastructure

**Completed**:
- ✅ Created directory structure
- ✅ Initialized tracking templates
- ✅ Set up CSV summary file
- ✅ Created decision log

---

## Phase 1: Factor Evolution (Loop 1-5)

**Objective**: Find factor combination with IC > 0.11
**Fixed Model**: LightGBM (SOTA configuration)
**Starting Point**: Price_Distance_Z (IC: 0.102)
**Expected Duration**: ~50 minutes

**Strategy**:
- Loop 1-2: Multi-timeframe expansion (3D, 40D, 60D Z-Score windows)
- Loop 3-4: Volume combined factors (Z × Volume, Z × VPT)
- Loop 5: Interaction terms (Z_diff, risk_adjusted Z)

**Factor Evolution Directions**:
1. **Multi-timeframe Z-Score**: Add 3D, 40D, 60D windows
2. **Volume-Price Interaction**: Z_Score × Volume_Ratio, Z_Score × VPT
3. **Interaction Terms**: Z_5D - Z_20D (short-long term diff)
4. **Risk-Adjusted**: Z_Score / Volatility_20D
5. **Market Regime**: Trend_Strength = |Z_5D| + |Z_10D| + |Z_20D|

**Constraints**:
- Max factors: 10
- Min IC per factor: 0.05
- Max correlation between factors: 0.7
- Max new factors per loop: 2

---

### Loop 1 - Multi-timeframe Expansion
**Time**: [Pending]
**Status**: 🔄 Starting

**New Factors to Test**:
- Price_Distance_Z_3D
- Price_Distance_Z_40D
- Price_Distance_Z_60D

**Hypothesis**: Extending Z-Score to more timeframes will capture both short-term signals (3D) and long-term trends (40D, 60D), potentially improving IC

**Expected Outcome**: IC improvement to ~0.105-0.108

---

[Subsequent loops will be appended here as experiment runs]

---

## Phase 2: Model Optimization (Loop 6-10)

**Objective**: Achieve returns > 5% with fixed best factors
**Status**: ⏳ Waiting for Phase 1 completion

---

## Phase 3: Joint Fine-tuning (Loop 11-15)

**Objective**: Balance all metrics (IC, returns, drawdown)
**Status**: ⏳ Waiting for Phase 2 completion

---

*Last Updated: 2026-01-23*
