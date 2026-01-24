"""
Generate reports from experimental results
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from rdagent.scenarios.qlib.exhaustive_search.shared.experiment_tracker import ExperimentTracker


class ReportGenerator:
    """Generate reports from experiment tracker"""

    def __init__(self, tracker: ExperimentTracker, output_dir: str = "results"):
        """
        Initialize report generator

        Args:
            tracker: Experiment tracker with results
            output_dir: Directory to save reports
        """
        self.tracker = tracker
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_layer1_report(self) -> str:
        """
        Generate Layer 1 summary report

        Returns:
            Path to generated report
        """
        # Get all experiments
        experiments = self.tracker.get_all_experiments()

        # Generate report path first
        report_path = self.output_dir / "layer1_report.md"

        if not experiments:
            # Write placeholder report
            report = f"""# Layer 1 Single Factor Scan Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

No experiments found. Run exhaustive search to generate results.

To start:
```bash
rdagent exhaustive_search --layers 1
```
"""
            with open(report_path, "w") as f:
                f.write(report)

            return str(report_path)

        # Calculate statistics
        total = len(experiments)
        completed = sum(1 for e in experiments if e["status"] == "completed")

        # Get best results
        best = experiments[0] if experiments else None

        # Generate markdown report
        report = f"""# Layer 1 Single Factor Scan Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

- **Total factors tested:** {total}
- **Successfully completed:** {completed}
- **Failed:** {total - completed}
- **Success rate:** {completed/total*100:.1f}%

## Best Result

| Metric | Value |
|--------|-------|
| Factor | {best['factors'] if best else 'N/A'} |
| **IC** | **{best['ic']:.4f}** if best else 'N/A' |
| IR | {best['ir']:.4f} if best else 'N/A' |
| Rank IC | {best['rank_ic']:.4f} if best else 'N/A' |
| Annual Return | {best['annual_return']*100:.2f}% if best else 'N/A' |
| Max Drawdown | {best['max_drawdown']*100:.2f}% if best else 'N/A' |
| Sharpe Ratio | {best['sharpe_ratio']:.4f} if best else 'N/A' |

## Top 10 Factors

| Rank | Factor | IC | IR | Return | Drawdown |
|------|--------|-----|----|----|----|
"""

        # Add top 10 table
        for i, exp in enumerate(experiments[:10], 1):
            factor_name = eval(exp["factors"])[0] if exp["factors"] else "Unknown"
            report += (
                f"| {i} | {factor_name} | {exp['ic']:.4f} | {exp['ir']:.4f} | "
                f"{exp['annual_return']*100:.2f}% | {exp['max_drawdown']*100:.2f}% |\n"
            )

        # Add insights
        report += "\n## Key Insights\n\n"

        if best and best['ic'] > 0.0985:
            improvement = (best['ic'] - 0.0985) / 0.0985 * 100
            report += f"- ✅ **SOTA exceeded**: Best factor ({best['factors']}) achieves IC={best['ic']:.4f}, "
            report += f"which is **{improvement:.1f}% better** than current SOTA (0.0985)\n\n"
        else:
            report += "- ⚠️ **SOTA not exceeded**: Current best IC is below target\n\n"

        # Save report (report_path already defined at top)
        with open(report_path, "w") as f:
            f.write(report)

        print(f"Report saved to: {report_path}")

        return str(report_path)

    def save_top_factors_csv(self, n: int = 20):
        """
        Save top N factors to CSV

        Args:
            n: Number of top factors to save
        """
        import csv

        experiments = self.tracker.get_all_experiments()[:n]

        csv_path = self.output_dir / "top_factors.csv"

        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Rank", "Factor", "IC", "IR", "Rank_IC",
                "Annual_Return", "Max_Drawdown", "Sharpe_Ratio"
            ])

            if not experiments:
                # Write empty row to indicate no data
                writer.writerow(["No experiments", "", "", "", "", "", "", ""])
            else:
                for i, exp in enumerate(experiments, 1):
                    factor_name = eval(exp["factors"])[0] if exp["factors"] else "Unknown"
                    writer.writerow([
                        i,
                        factor_name,
                        f"{exp['ic']:.6f}",
                        f"{exp['ir']:.6f}",
                        f"{exp['rank_ic']:.6f}",
                        f"{exp['annual_return']:.6f}",
                        f"{exp['max_drawdown']:.6f}",
                        f"{exp['sharpe_ratio']:.6f}",
                    ])

        print(f"CSV saved to: {csv_path}")
        return str(csv_path)
