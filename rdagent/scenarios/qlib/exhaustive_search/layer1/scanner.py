"""
Layer 1: Single factor systematic scanner
"""
import asyncio
from typing import List, Dict

from rdagent.scenarios.qlib.exhaustive_search.layer1.factor_library import FactorLibrary
from rdagent.scenarios.qlib.exhaustive_search.layer1.experiment_runner import SingleFactorRunner
from rdagent.scenarios.qlib.exhaustive_search.shared.experiment_tracker import ExperimentTracker
from rdagent.log import rdagent_logger as logger


class Layer1Scanner:
    """Systematically scan and evaluate all single factors"""

    def __init__(
        self,
        tracker: ExperimentTracker,
        max_parallel: int = 4,
    ):
        """
        Initialize Layer 1 scanner

        Args:
            tracker: Experiment tracker for recording results
            max_parallel: Maximum number of parallel experiments
        """
        self.tracker = tracker
        self.max_parallel = max_parallel

        # Load factor library
        self.factor_lib = FactorLibrary()
        self.factors = self.factor_lib.get_all_factors()

        # Initialize runner
        self.runner = SingleFactorRunner()

        logger.info(f"Layer1Scanner initialized with {len(self.factors)} factors")

    async def scan_all_factors(self):
        """Scan all factors in the library"""
        logger.info(f"Starting systematic scan of {len(self.factors)} factors")
        logger.info(f"Max parallel: {self.max_parallel}")

        completed = 0
        failed = 0

        for factor in self.factors:
            factor_name = factor["name"]

            # Check if already tested
            existing = self.tracker.get_experiments_by_factor(factor_name)
            if existing and existing[0]["status"] == "completed":
                logger.info(f"Skipping {factor_name} (already tested)")
                completed += 1
                continue

            # Test the factor
            result = await self.test_factor_async(factor)

            if result["status"] == "completed":
                completed += 1
            else:
                failed += 1

            # Progress update
            total_tested = completed + failed
            logger.info(
                f"Progress: {total_tested}/{len(self.factors)} "
                f"(Completed: {completed}, Failed: {failed})"
            )

        # Generate summary
        self.generate_summary(completed, failed)

    async def test_factor_async(self, factor: Dict) -> Dict:
        """
        Test a single factor asynchronously

        Args:
            factor: Factor dictionary with name, formula, description

        Returns:
            Test result dictionary
        """
        factor_name = factor["name"]
        factor_formula = factor["formula"]
        factor_description = factor.get("description", factor_name)

        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            self.runner.test_single_factor,
            factor_name,
            factor_formula,
            factor_description
        )

        # Record in database
        if result["status"] == "completed":
            self.tracker.record_experiment(
                factors=[factor_name],
                factor_formulas={factor_name: factor_formula},
                model="LightGBM",
                hyperparameters={"learning_rate": 0.2},
                ic=result.get("ic", 0.0),
                ir=result.get("ir", 0.0),
                rank_ic=result.get("rank_ic", 0.0),
                annual_return=result.get("annual_return", 0.0),
                max_drawdown=result.get("max_drawdown", 0.0),
                sharpe_ratio=result.get("sharpe_ratio", 0.0),
                training_time=result.get("training_time", 0.0),
                status=result["status"],
                layer="layer1"
            )

        return result

    def generate_summary(self, completed: int, failed: int):
        """Generate summary report"""
        logger.info("=" * 60)
        logger.info("Layer 1 Scan Summary")
        logger.info("=" * 60)
        logger.info(f"Total factors: {len(self.factors)}")
        logger.info(f"Completed: {completed}")
        logger.info(f"Failed: {failed}")
        logger.info(f"Success rate: {completed/(completed+failed)*100:.1f}%")

        # Get best results
        best = self.tracker.get_best_ic()
        if best:
            logger.info(f"Best IC: {best['ic']:.4f} ({best['factors']})")

        logger.info("=" * 60)

    def get_top_factors(self, n: int = 10) -> List[Dict]:
        """
        Get top N factors by IC

        Args:
            n: Number of top factors to return

        Returns:
            List of top factor experiments
        """
        all_exps = self.tracker.get_all_experiments()
        return all_exps[:n]
