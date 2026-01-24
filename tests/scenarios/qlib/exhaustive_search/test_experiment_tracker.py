# tests/scenarios/qlib/exhaustive_search/test_experiment_tracker.py
import pytest
import tempfile
from pathlib import Path

from rdagent.scenarios.qlib.exhaustive_search.shared.experiment_tracker import ExperimentTracker


@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        yield db_path


def test_experiment_tracker_creation(temp_db):
    """Test that ExperimentTracker can be created"""
    tracker = ExperimentTracker(temp_db)
    assert tracker.db is not None
    assert temp_db.exists()


def test_record_experiment(temp_db):
    """Test recording a single experiment"""
    tracker = ExperimentTracker(temp_db)

    tracker.record_experiment(
        factors=["Momentum_5D"],
        factor_formulas={"Momentum_5D": "close/REF(close,5)-1"},
        model="LightGBM",
        hyperparameters={"learning_rate": 0.2},
        ic=0.095,
        ir=0.5,
        rank_ic=0.045,
        annual_return=-0.024,
        max_drawdown=0.15,
        sharpe_ratio=-0.3,
        training_time=120.5,
        status="completed"
    )

    # Verify it was recorded
    results = tracker.get_all_experiments()
    assert len(results) == 1
    assert results[0]["ic"] == 0.095


def test_get_best_ic(temp_db):
    """Test getting best IC result"""
    tracker = ExperimentTracker(temp_db)

    # Record multiple experiments
    tracker.record_experiment(
        factors=["Factor_A"],
        factor_formulas={},
        model="LGB",
        hyperparameters={},
        ic=0.090,
        ir=0.4,
        rank_ic=0.04,
        annual_return=-0.03,
        max_drawdown=0.2,
        sharpe_ratio=-0.4,
        training_time=100,
        status="completed"
    )

    tracker.record_experiment(
        factors=["Factor_B"],
        factor_formulas={},
        model="LGB",
        hyperparameters={},
        ic=0.105,  # Better
        ir=0.6,
        rank_ic=0.05,
        annual_return=-0.01,
        max_drawdown=0.1,
        sharpe_ratio=-0.1,
        training_time=110,
        status="completed"
    )

    best = tracker.get_best_ic()
    assert best["ic"] == 0.105
    # JSON uses double quotes
    assert best["factors"] == '["Factor_B"]'
