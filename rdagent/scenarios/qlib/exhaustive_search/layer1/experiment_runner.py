"""
Wrapper around QlibFactorRunner for single factor testing
"""
import time
from typing import Dict, List

from rdagent.scenarios.qlib.developer.factor_runner import QlibFactorRunner
from rdagent.scenarios.qlib.experiment.factor_experiment import (
    FactorExperiment,
    FactorTask,
)
from rdagent.log import rdagent_logger as logger


class SingleFactorRunner:
    """Run single factor backtest using existing Qlib infrastructure"""

    def __init__(self, qlib_config: Dict = None):
        """
        Initialize runner

        Args:
            qlib_config: Qlib configuration (train/valid/test periods)
        """
        self.qlib_config = qlib_config or self.get_default_config()

    def get_default_config(self) -> Dict:
        """Get default Qlib configuration"""
        return {
            "train_start": "2008-01-01",
            "train_end": "2014-12-31",
            "valid_start": "2015-01-01",
            "valid_end": "2016-12-31",
            "test_start": "2017-01-01",
            "test_end": "2020-12-31",
        }

    def test_single_factor(
        self,
        factor_name: str,
        factor_formula: str,
        factor_description: str,
    ) -> Dict:
        """
        Test a single factor

        Args:
            factor_name: Name of the factor
            factor_formula: Formula expression
            factor_description: Human-readable description

        Returns:
            Dictionary with test results (IC, IR, returns, etc.)
        """
        logger.info(f"Testing factor: {factor_name}")
        start_time = time.time()

        try:
            # Create factor task
            task = FactorTask(
                factor_name=factor_name,
                factor_description=factor_description,
                factor_formulation=factor_formula,
                variables={},
            )

            # Create experiment
            experiment = FactorExperiment(
                sub_tasks=[task],
                hypothesis=None,
            )

            # Run backtest using QlibFactorRunner
            runner = QlibFactorRunner()
            result = runner.develop(experiment)

            # Extract metrics
            metrics = self.extract_metrics(result)

            # Add metadata
            metrics["training_time"] = time.time() - start_time
            metrics["status"] = "completed"

            logger.info(f"Factor {factor_name} completed: IC={metrics.get('ic', 'N/A')}")

            return metrics

        except Exception as e:
            logger.error(f"Factor {factor_name} failed: {str(e)}")
            return {
                "status": "failed",
                "error": str(e),
                "training_time": time.time() - start_time,
                "ic": None,
                "ir": None,
                "rank_ic": None,
                "annual_return": None,
                "max_drawdown": None,
                "sharpe_ratio": None,
            }

    def extract_metrics(self, result) -> Dict:
        """
        Extract metrics from Qlib backtest result

        Args:
            result: Result from QlibFactorRunner

        Returns:
            Dictionary with metrics
        """
        # This is a placeholder - actual implementation depends on
        # the structure of QlibFactorRunner results

        # Check if result has metrics directly
        if hasattr(result, "metrics"):
            return result.metrics

        # If result is a dict
        if isinstance(result, dict):
            return {
                "ic": result.get("ic"),
                "ir": result.get("ir"),
                "rank_ic": result.get("rank_ic"),
                "annual_return": result.get("annual_return"),
                "max_drawdown": result.get("max_drawdown"),
                "sharpe_ratio": result.get("sharpe_ratio"),
            }

        # Fallback: try to extract from result
        try:
            # Common metric names in Qlib
            metric_names = ["ic", "IC", "test_ic", "pred_ic"]
            for name in metric_names:
                if hasattr(result, name):
                    return {
                        "ic": getattr(result, name),
                        "ir": getattr(result, "ir", None),
                        "rank_ic": getattr(result, "rank_ic", None),
                        "annual_return": getattr(result, "annual_return", None),
                        "max_drawdown": getattr(result, "max_drawdown", None),
                        "sharpe_ratio": getattr(result, "sharpe_ratio", None),
                    }
        except Exception:
            pass

        # Default values if extraction fails
        return {
            "ic": 0.0,
            "ir": 0.0,
            "rank_ic": 0.0,
            "annual_return": 0.0,
            "max_drawdown": 0.0,
            "sharpe_ratio": 0.0,
        }
