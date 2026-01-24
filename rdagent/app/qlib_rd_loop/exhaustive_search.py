"""
Main entry point for exhaustive search functionality
"""
import asyncio
import fire
from pathlib import Path

from rdagent.scenarios.qlib.exhaustive_search.layer1.scanner import Layer1Scanner
from rdagent.scenarios.qlib.exhaustive_search.shared.experiment_tracker import ExperimentTracker
from rdagent.scenarios.qlib.exhaustive_search.shared.report_generator import ReportGenerator
from rdagent.log import rdagent_logger as logger


class ExhaustiveSearchLoop:
    """Main loop for exhaustive search experiments"""

    def __init__(
        self,
        layers: str = "1",
        max_parallel: int = 4,
        workspace: str = "git_ignore_folder/exhaustive_search_workspace",
        results_dir: str = "results"
    ):
        """
        Initialize exhaustive search loop

        Args:
            layers: Comma-separated list of layers to run (e.g., "1,2,3")
            max_parallel: Maximum parallel experiments
            workspace: Working directory
            results_dir: Results output directory
        """
        self.layer_list = [int(l.strip()) for l in layers.split(",")]
        self.max_parallel = max_parallel
        self.workspace = Path(workspace)
        self.results_dir = Path(results_dir)

        # Create directories
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.tracker = ExperimentTracker(self.results_dir / "experiments.db")
        self.reporter = ReportGenerator(self.tracker, self.results_dir)

        logger.info(f"ExhaustiveSearchLoop initialized")
        logger.info(f"Layers: {self.layer_list}")
        logger.info(f"Max parallel: {self.max_parallel}")
        logger.info(f"Results dir: {self.results_dir}")

    async def run_full_pipeline(self):
        """Run full pipeline for specified layers"""
        logger.info("🚀 Starting exhaustive search")

        if 1 in self.layer_list:
            await self.run_layer1()

        logger.info("✅ Exhaustive search completed")

    async def run_layer1(self):
        """Run Layer 1: Single factor scanning"""
        logger.info("=" * 60)
        logger.info("🔍 Layer 1: Single Factor Systematic Scan")
        logger.info("=" * 60)

        scanner = Layer1Scanner(
            tracker=self.tracker,
            max_parallel=self.max_parallel
        )

        await scanner.scan_all_factors()

        # Generate report
        logger.info("Generating Layer 1 report...")
        self.reporter.generate_layer1_report()
        self.reporter.save_top_factors_csv()


def main(
    layers: str = "1",
    max_parallel: int = 4,
    results_dir: str = "results"
):
    """
    Start exhaustive search experiment

    Examples:
        # Run Layer 1 with default settings
        python rdagent/app/qlib_rd_loop/exhaustive_search.py

        # Run with high parallelism
        python rdagent/app/qlib_rd_loop/exhaustive_search.py --max_parallel 8
    """
    loop = ExhaustiveSearchLoop(
        layers=layers,
        max_parallel=max_parallel,
        results_dir=results_dir
    )

    asyncio.run(loop.run_full_pipeline())


if __name__ == "__main__":
    fire.Fire(main)
