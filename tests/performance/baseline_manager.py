"""Baseline management utility for performance regression testing.

This script manages performance baselines and compares current
measurements against stored baselines to detect regressions.

Usage:
    python baseline_manager.py --action list           # List all baselines
    python baseline_manager.py --action compare         # Compare vs baselines
    python baseline_manager.py --action reset           # Reset all baselines
    python baseline_manager.py --action export          # Export to JSON
"""
import json
import argparse
from pathlib import Path
from typing import Optional, Dict, List


BASELINES_FILE = Path(__file__).parent / "baselines" / "performance.json"


class BaselineManager:
    """Manage performance baselines."""

    def __init__(self, baseline_file: Path = BASELINES_FILE):
        """Initialize manager.

        Args:
            baseline_file: Path to baseline JSON file
        """
        self.baseline_file = baseline_file
        self.baseline_file.parent.mkdir(exist_ok=True)
        self._load()

    def _load(self):
        """Load baselines from file."""
        self.baselines = {}
        if self.baseline_file.exists():
            try:
                self.baselines = json.loads(self.baseline_file.read_text())
            except (json.JSONDecodeError, IOError):
                pass

    def _save(self):
        """Save baselines to file."""
        self.baseline_file.write_text(json.dumps(self.baselines, indent=2))

    def list_baselines(self) -> Dict:
        """List all baselines.

        Returns:
            Dict of baseline names and metrics
        """
        return self.baselines

    def compare_measurement(
        self,
        test_name: str,
        actual_ms: float,
        regression_threshold_pct: float = 20,
    ) -> Dict:
        """Compare measurement against baseline.

        Args:
            test_name: Name of the test
            actual_ms: Actual measured latency in milliseconds
            regression_threshold_pct: Allowed regression percentage

        Returns:
            Dict with comparison results
        """
        baseline = self.baselines.get(test_name)
        if baseline is None:
            return {
                "test_name": test_name,
                "status": "no_baseline",
                "message": f"No baseline found for {test_name}",
            }

        baseline_ms = baseline.get("duration_ms", 0)
        regression_pct = ((actual_ms - baseline_ms) / baseline_ms) * 100 if baseline_ms > 0 else 0

        is_regression = regression_pct > regression_threshold_pct
        status = "regression" if is_regression else "pass"

        return {
            "test_name": test_name,
            "status": status,
            "baseline_ms": baseline_ms,
            "actual_ms": actual_ms,
            "regression_pct": regression_pct,
            "threshold_pct": regression_threshold_pct,
            "message": (
                f"Regression detected: +{regression_pct:.1f}% "
                f"({actual_ms:.0f}ms vs baseline {baseline_ms:.0f}ms)"
                if is_regression
                else f"OK: {actual_ms:.0f}ms (baseline {baseline_ms:.0f}ms, +{regression_pct:.1f}%)"
            ),
        }

    def compare_all_measurements(
        self,
        measurements: Dict[str, float],
        regression_threshold_pct: float = 20,
    ) -> Dict:
        """Compare multiple measurements against baselines.

        Args:
            measurements: Dict of {test_name: actual_ms}
            regression_threshold_pct: Allowed regression percentage

        Returns:
            Dict with comparison results for each test
        """
        results = {
            "total_tests": len(measurements),
            "regressions": 0,
            "passes": 0,
            "no_baselines": 0,
            "details": [],
        }

        for test_name, actual_ms in measurements.items():
            comparison = self.compare_measurement(
                test_name,
                actual_ms,
                regression_threshold_pct,
            )
            results["details"].append(comparison)

            if comparison["status"] == "regression":
                results["regressions"] += 1
            elif comparison["status"] == "pass":
                results["passes"] += 1
            else:
                results["no_baselines"] += 1

        return results

    def update_baseline(self, test_name: str, metrics: Dict):
        """Update a baseline.

        Args:
            test_name: Name of the test
            metrics: Metrics dict with at least duration_ms
        """
        self.baselines[test_name] = metrics
        self._save()

    def reset_baselines(self):
        """Reset all baselines."""
        self.baselines = {}
        self._save()

    def export_baselines(self, output_file: Path):
        """Export baselines to file.

        Args:
            output_file: Path to export JSON file
        """
        output_file.write_text(json.dumps(self.baselines, indent=2))

    def import_baselines(self, input_file: Path):
        """Import baselines from file.

        Args:
            input_file: Path to import JSON file
        """
        try:
            imported = json.loads(input_file.read_text())
            self.baselines.update(imported)
            self._save()
        except (json.JSONDecodeError, IOError) as e:
            raise ValueError(f"Failed to import baselines: {e}")

    def get_summary(self) -> Dict:
        """Get summary statistics of baselines.

        Returns:
            Dict with summary stats
        """
        if not self.baselines:
            return {
                "total_baselines": 0,
                "median_ms": 0,
                "min_ms": 0,
                "max_ms": 0,
            }

        latencies = [b.get("duration_ms", 0) for b in self.baselines.values()]
        latencies.sort()

        return {
            "total_baselines": len(self.baselines),
            "median_ms": latencies[len(latencies) // 2],
            "min_ms": min(latencies),
            "max_ms": max(latencies),
            "avg_ms": sum(latencies) / len(latencies),
        }


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Manage performance baselines"
    )
    parser.add_argument(
        "--action",
        choices=["list", "compare", "reset", "export", "summary"],
        default="list",
        help="Action to perform",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file for export action",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=20,
        help="Regression threshold percentage (default 20)",
    )

    args = parser.parse_args()

    manager = BaselineManager()

    if args.action == "list":
        baselines = manager.list_baselines()
        if baselines:
            print("Performance Baselines:\n")
            for name, metrics in baselines.items():
                print(f"  {name}")
                print(f"    Duration: {metrics.get('duration_ms', 0):.2f}ms")
                if metrics.get("timestamp"):
                    print(f"    Timestamp: {metrics['timestamp']}")
        else:
            print("No baselines found.")

    elif args.action == "summary":
        summary = manager.get_summary()
        print("\nBaseline Summary:\n")
        for key, value in summary.items():
            print(f"  {key}: {value:.2f}ms" if isinstance(value, float) else f"  {key}: {value}")

    elif args.action == "reset":
        manager.reset_baselines()
        print("Baselines reset.")

    elif args.action == "export":
        if not args.output:
            print("Error: --output required for export")
            return 1
        manager.export_baselines(args.output)
        print(f"Baselines exported to {args.output}")

    elif args.action == "compare":
        print("Comparison not implemented in CLI. Use pytest to run tests.")

    return 0


if __name__ == "__main__":
    exit(main())
