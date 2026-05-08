import argparse
import json
import logging
from pathlib import Path

from app.common_queries import COMMON_GROCERY_SEARCHES
from app.kroger.spider import run_kroger_batch

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

DEFAULT_OUTPUT = Path(__file__).with_name("spider_results") / "kroger_products.jsonl"


def write_jsonl(items: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item) + "\n")


def main(argv: list[str] | None = None):
    parser = argparse.ArgumentParser(description="Run Kroger batch grocery searches.")
    parser.add_argument("--location-id", default="01100260", help="Kroger store location id (default: 01100260)")
    parser.add_argument("--max-results", type=int, default=10, help="Maximum products per search query")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output JSONL file path")
    args = parser.parse_args(argv)

    queries = list(COMMON_GROCERY_SEARCHES)

    print(f"Starting Kroger batch search for: {', '.join(queries)}")
    print(f"Store: {args.location_id}")

    results = run_kroger_batch(
        queries=queries,
        location_id=args.location_id,
        max_results=args.max_results,
    )

    print(f"\nFound {len(results)} total items.")
    print(f"Saving to {args.output}...")

    write_jsonl(results, args.output)

    print(f"Success! You can now view the output in {args.output}")


if __name__ == "__main__":
    main()
