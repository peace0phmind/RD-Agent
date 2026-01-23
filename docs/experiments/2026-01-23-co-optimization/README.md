# Factor-Model Co-optimization Experiment

**Date**: 2026-01-23
**Objective**: Achieve IC > 0.11, Returns > 5%, Drawdown < 10%
**Approach**: Iterative co-optimization (3-phase)
**Status**: 🚀 In Progress

## Quick Links

- [Real-time Log](real_time_log.md) - Live experiment updates
- [Loop Summary](loop_summary.csv) - Quantitative results per loop
- [Decision Log](decision_log.md) - Key decisions and rationale
- [Lessons Learned](lessons_learned.md) - Insights for future experiments

## Experiment Structure

```
Phase 1 (Loop 1-5): Factor Evolution with Fixed Model
  Model: LightGBM SOTA
  Target: IC > 0.11
  ↓
Phase 2 (Loop 6-10): Model Optimization with Fixed Factors
  Factors: Best from Phase 1
  Target: Returns > 5%
  ↓
Phase 3 (Loop 11-15): Joint Fine-tuning
  Target: Balance all metrics
```

## Baseline (from previous experiments)

- Starting IC: 0.102 (Price_Distance_Z factor)
- Starting Returns: -2.42%
- Model: LightGBM SOTA
- Max Drawdown: 0.00%

## Targets

| Metric | Baseline | Target | Status |
|--------|----------|--------|--------|
| IC | 0.102 | **> 0.11** | 🎯 Pending |
| Annual Returns | -2.42% | **> 5%** | 🎯 Pending |
| Max Drawdown | 0.00% | **< 10%** | ✅ OK |
| Cross-period Stability | Unknown | **All profitable** | 🎯 Pending |

## Execution Timeline

- **Phase 1**: ~50 minutes (5 loops)
- **Phase 2**: ~40 minutes (5 loops)
- **Phase 3**: ~40 minutes (5 loops)
- **Total**: ~2.5 hours

## Progress

- [x] Planning completed
- [x] Implementation plan created
- [ ] Phase 1: In progress...
- [ ] Phase 2: Pending
- [ ] Phase 3: Pending

---

*Last Updated: 2026-01-23*
