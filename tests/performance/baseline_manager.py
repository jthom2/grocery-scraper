# cli tool for managing and comparing performance baselines
try:
    import orjson
except ImportError:
    import json as orjson
import argparse
from pathlib import Path
from typing import Optional, Dict, List


BASELINES_FILE = Path(__file__).parent / "baselines" / "performance.json"


# persists and compares performance metrics across runs
class BaselineManager:
    def __init__(self, baseline_file: Path = BASELINES_FILE):
        self.baseline_file = baseline_file
        self.baseline_file.parent.mkdir(exist_ok=True)
        self._load()

    def _load(self):
        self.baselines = {}
        if self.baseline_file.exists():
            try:
                self.baselines = orjson.loads(self.baseline_file.read_bytes())
            except (orjson.JSONDecodeError, IOError):
                pass

    def _save(self):
        self.baseline_file.write_bytes(orjson.dumps(self.baselines, option=orjson.OPT_INDENT_2))

    def list_baselines(self) -> Dict:
        return self.baselines

    # returns pass/regression status with detailed breakdown
    def compare_measurement(
        self,
        test_name: str,
        actual_ms: float,
        regression_threshold_pct: float = 20,
    ) -> Dict:
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

    # batch comparison for running full test suite
    def compare_all_measurements(
        self,
        measurements: Dict[str, float],
        regression_threshold_pct: float = 20,
    ) -> Dict:
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
        self.baselines[test_name] = metrics
        self._save()

    def reset_baselines(self):
        self.baselines = {}
        self._save()

    def export_baselines(self, output_file: Path):
        output_file.write_bytes(orjson.dumps(self.baselines, option=orjson.OPT_INDENT_2))

    def import_baselines(self, input_file: Path):
        try:
            imported = orjson.loads(input_file.read_bytes())
            self.baselines.update(imported)
            self._save()
        except (orjson.JSONDecodeError, IOError) as e:
            raise ValueError(f"Failed to import baselines: {e}")

    def get_summary(self) -> Dict:
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
