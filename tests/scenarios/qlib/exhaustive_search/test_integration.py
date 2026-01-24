"""
Integration tests for Phase 1 exhaustive search
"""
import pytest
import tempfile
from pathlib import Path

from rdagent.app.qlib_rd_loop.exhaustive_search import ExhaustiveSearchLoop
import asyncio


@pytest.fixture
def temp_results():
    """Create temporary results directory"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.mark.slow
def test_full_layer1_pipeline(temp_results):
    """Test complete Layer 1 pipeline with small subset"""
    loop = ExhaustiveSearchLoop(
        layers="1",
        max_parallel=2,
        results_dir=str(temp_results)
    )

    # Run pipeline
    asyncio.run(loop.run_full_pipeline())

    # Verify database was created
    db_path = temp_results / "experiments.db"
    assert db_path.exists()

    # Verify reports were generated
    report_path = temp_results / "layer1_report.md"
    assert report_path.exists()

    csv_path = temp_results / "top_factors.csv"
    assert csv_path.exists()

    # Verify database has experiments
    tracker = loop.tracker
    experiments = tracker.get_all_experiments()
    assert len(experiments) > 0


@pytest.mark.slow
def test_experiment_tracker_deduplication(temp_results):
    """Test that duplicate experiments are not recorded"""
    from rdagent.scenarios.qlib.exhaustive_search.shared.experiment_tracker import ExperimentTracker

    tracker = ExperimentTracker(temp_results / "test.db")

    # Record same experiment twice
    id1 = tracker.record_experiment(
        factors=["TEST_FACTOR"],
        factor_formulas={"TEST_FACTOR": "test"},
        model="LGB",
        hyperparameters={},
        ic=0.1,
        ir=0.5,
        rank_ic=0.05,
        annual_return=-0.02,
        max_drawdown=0.1,
        sharpe_ratio=-0.3,
        training_time=100,
        status="completed"
    )

    id2 = tracker.record_experiment(
        factors=["TEST_FACTOR"],
        factor_formulas={"TEST_FACTOR": "test"},
        model="LGB",
        hyperparameters={},
        ic=0.1,
        ir=0.5,
        rank_ic=0.05,
        annual_return=-0.02,
        max_drawdown=0.1,
        sharpe_ratio=-0.3,
        training_time=100,
        status="completed"
    )

    # Second should return -1 (duplicate)
    assert id1 > 0
    assert id2 == -1

    # Only one experiment in database
    experiments = tracker.get_all_experiments()
    assert len(experiments) == 1
