#!/usr/bin/env python3
# measures search latency across retailers to track optimization progress
import argparse
import cProfile
import io
import json
import pstats
import sys
import time
from collections import defaultdict
from contextlib import contextmanager
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))


# stores elapsed ms keyed by name for later aggregation
@contextmanager
def timer(name, timings):
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    timings[name].append(elapsed * 1000)  # Convert to milliseconds


# collects timing data across multiple search iterations
class PerformanceProfiler:
    def __init__(self):
        self.timings = defaultdict(list)
        self.results_count = {}
        self.errors = {}

    # walmart uses simple http fetcher, typically fastest
    def profile_walmart(self, query, max_results=5):
        from app.walmart import search_products

        print(f"\n{'='*60}")
        print(f"Profiling Walmart: '{query}'")
        print(f"{'='*60}")

        with timer("walmart.total", self.timings):
            with timer("walmart.search", self.timings):
                results = search_products.search(query, max_results=max_results)

            self.results_count["walmart"] = len(results)

        return results

    # kroger requires stealthyfetcher, expect higher latency
    def profile_kroger(self, query, max_results=5):
        from app.kroger import search_products

        print(f"\n{'='*60}")
        print(f"Profiling Kroger: '{query}'")
        print(f"{'='*60}")

        with timer("kroger.total", self.timings):
            with timer("kroger.search", self.timings):
                results = search_products.search(query, max_results=max_results)

            self.results_count["kroger"] = len(results)

        return results

    # publix tries fast path first, falls back to stealthyfetcher
    def profile_publix(self, query, max_results=5):
        from app.publix import search_products

        print(f"\n{'='*60}")
        print(f"Profiling Publix: '{query}'")
        print(f"{'='*60}")

        with timer("publix.total", self.timings):
            with timer("publix.search", self.timings):
                results = search_products.search(query, max_results=max_results)

            self.results_count["publix"] = len(results)

        return results

    # aldi has 7-request sequential flow, breakdown helps find bottlenecks
    def profile_aldi(self, query, max_results=5, zip_code=None):
        from app.aldi import search_products

        print(f"\n{'='*60}")
        print(f"Profiling Aldi: '{query}'")
        print(f"{'='*60}")

        with timer("aldi.total", self.timings):
            # Detailed timing for Aldi's sequential flow
            with timer("aldi.search_context", self.timings):
                search_context = search_products.build_search_context(
                    query, zip_code=zip_code
                )

            if not search_context:
                print("ERROR: Failed to build search context")
                self.errors["aldi"] = "Search context failed"
                return []

            with timer("aldi.search_placements", self.timings):
                placements = search_products.fetch_search_placements(
                    query,
                    search_context["zip_code"],
                    search_context["location_id"],
                    search_context["token"],
                    search_context["cookies"],
                    search_context["referer"],
                    max_results=max_results,
                )

            with timer("aldi.extract_item_ids", self.timings):
                item_ids = search_products.extract_item_ids(
                    placements, max_ids=max(max_results * 8, 24)
                )

            with timer("aldi.fetch_items", self.timings):
                results = []
                if item_ids:
                    batch_size = max(max_results * 2, 8)
                    for offset in range(0, len(item_ids), batch_size):
                        batch_ids = item_ids[offset : offset + batch_size]
                        items = search_products.fetch_items(
                            batch_ids,
                            search_context["location_id"],
                            search_context["zip_code"],
                            search_context["cookies"],
                            search_context["referer"],
                        )
                        if items:
                            for item in items:
                                if item.get("name"):
                                    results.append(
                                        search_products.normalize_item(
                                            item, search_context["location_id"]
                                        )
                                    )
                                    if len(results) >= max_results:
                                        break
                        if len(results) >= max_results:
                            break

            self.results_count["aldi"] = len(results)

        return results

    # formats timing stats for terminal output
    def print_summary(self):
        print(f"\n{'='*70}")
        print(f"{'PERFORMANCE SUMMARY':^70}")
        print(f"{'='*70}\n")

        # Print timing breakdown
        for retailer in ["walmart", "kroger", "publix", "aldi"]:
            retailer_timings = {
                k: v for k, v in self.timings.items() if k.startswith(retailer)
            }
            if not retailer_timings:
                continue

            print(f"\n{retailer.upper()} ({self.results_count.get(retailer, 0)} results)")
            print("-" * 70)

            for key, values in sorted(retailer_timings.items()):
                operation = key.split(".", 1)[1]
                avg = sum(values) / len(values)
                min_val = min(values)
                max_val = max(values)
                print(
                    f"  {operation:30} {avg:8.2f}ms  "
                    f"(min: {min_val:6.2f}ms, max: {max_val:6.2f}ms)"
                )

        # Cross-retailer comparison
        print(f"\n{'CROSS-RETAILER COMPARISON':^70}")
        print("-" * 70)
        print(f"{'Retailer':<15} {'Avg Time':<15} {'Results':<10} {'Status'}")
        print("-" * 70)

        for retailer in ["walmart", "kroger", "publix", "aldi"]:
            total_key = f"{retailer}.total"
            if total_key in self.timings:
                values = self.timings[total_key]
                avg = sum(values) / len(values)
                count = self.results_count.get(retailer, 0)
                status = self.errors.get(retailer, "OK")
                print(f"{retailer:<15} {avg:8.2f}ms      {count:<10} {status}")

        print(f"\n{'='*70}\n")

    # persists results for tracking performance over time
    def save_results(self, filepath):
        results = {
            "timings": {k: list(v) for k, v in self.timings.items()},
            "results_count": self.results_count,
            "errors": self.errors,
            "summary": {
                retailer: {
                    "avg_ms": sum(self.timings[f"{retailer}.total"])
                    / len(self.timings[f"{retailer}.total"])
                    if f"{retailer}.total" in self.timings
                    else None,
                    "results": self.results_count.get(retailer, 0),
                }
                for retailer in ["walmart", "kroger", "publix", "aldi"]
                if f"{retailer}.total" in self.timings
            },
        }

        with open(filepath, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to: {filepath}")


# identifies hot functions for targeted optimization
def run_with_cpu_profiling(func):
    profiler = cProfile.Profile()
    profiler.enable()
    result = func()
    profiler.disable()

    # Print stats
    s = io.StringIO()
    stats = pstats.Stats(profiler, stream=s)
    stats.sort_stats("cumulative")
    stats.print_stats(30)  # Top 30 functions

    print(f"\n{'='*70}")
    print(f"{'CPU PROFILING RESULTS':^70}")
    print(f"{'='*70}\n")
    print(s.getvalue())

    return result


def main():
    parser = argparse.ArgumentParser(description="Profile scraper performance")
    parser.add_argument(
        "--retailer",
        choices=["walmart", "kroger", "publix", "aldi", "all"],
        default="all",
        help="Retailer to profile",
    )
    parser.add_argument("--query", default="milk", help="Search query")
    parser.add_argument(
        "--max-results", type=int, default=5, help="Max results to fetch"
    )
    parser.add_argument(
        "--iterations", type=int, default=1, help="Number of iterations"
    )
    parser.add_argument(
        "--zip-code", help="ZIP code for Aldi (optional, uses default if not provided)"
    )
    parser.add_argument(
        "--profile-cpu", action="store_true", help="Enable CPU profiling with cProfile"
    )
    parser.add_argument(
        "--save-json", help="Save results to JSON file (e.g., results.json)"
    )

    args = parser.parse_args()

    profiler = PerformanceProfiler()

    retailers = (
        ["walmart", "kroger", "publix", "aldi"]
        if args.retailer == "all"
        else [args.retailer]
    )

    for iteration in range(args.iterations):
        if args.iterations > 1:
            print(f"\n\n{'#'*70}")
            print(f"{'ITERATION ' + str(iteration + 1) + ' of ' + str(args.iterations):^70}")
            print(f"{'#'*70}")

        for retailer in retailers:
            try:
                if args.profile_cpu and args.iterations == 1:

                    def profile_func():
                        if retailer == "walmart":
                            return profiler.profile_walmart(
                                args.query, args.max_results
                            )
                        elif retailer == "kroger":
                            return profiler.profile_kroger(args.query, args.max_results)
                        elif retailer == "publix":
                            return profiler.profile_publix(args.query, args.max_results)
                        elif retailer == "aldi":
                            return profiler.profile_aldi(
                                args.query, args.max_results, args.zip_code
                            )

                    run_with_cpu_profiling(profile_func)
                else:
                    if retailer == "walmart":
                        profiler.profile_walmart(args.query, args.max_results)
                    elif retailer == "kroger":
                        profiler.profile_kroger(args.query, args.max_results)
                    elif retailer == "publix":
                        profiler.profile_publix(args.query, args.max_results)
                    elif retailer == "aldi":
                        profiler.profile_aldi(args.query, args.max_results, args.zip_code)

            except Exception as e:
                print(f"ERROR profiling {retailer}: {e}")
                profiler.errors[retailer] = str(e)
                import traceback

                traceback.print_exc()

    # Print summary
    profiler.print_summary()

    # Save results if requested
    if args.save_json:
        profiler.save_results(args.save_json)


if __name__ == "__main__":
    main()
