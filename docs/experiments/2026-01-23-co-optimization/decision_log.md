# Key Decisions Log

## Decision 0: Experiment Approach

**Time**: 2026-01-23 (Planning phase)
**Context**: Need to find effective factor-model combination with balanced IC and returns

**Options**:
- **A: Iterative co-optimization** (factor → model → joint)
  - Pros: Computationally efficient (2-3 hours), easy to debug
  - Cons: May miss some factor-model combinations
- **B: Synchronous joint evolution** (factor + model together)
  - Pros: Theoretical global optimum
  - Cons: Very slow (4-6 hours), hard to debug
- **C: Hierarchical** (factor then model)
  - Pros: Simple, controlled
  - Cons: Ignores interaction effects

**Selection**: ✅ **A (Iterative co-optimization)**

**Rationale**:
1. Computationally efficient - fits within 2-3 hours
2. Easy to debug and trace issues
3. Each component gets fully optimized before moving on
4. Proven effective in prior experiments (3-loop baseline showed promise)

**Expected Outcome**: IC > 0.11 and Returns > 5% within 15 loops

**Contingency Plan**: If IC < 0.105 after Phase 1, consider extending Phase 1 or switching to approach B

---

*This log will be updated as we make key decisions during the experiment*
