# Grocery Scraper

Grocery Scraper is a Python 3.12 toolkit for collecting and normalizing grocery product data across ALDI, Kroger, Publix, and Walmart. It exposes the same retailer clients through a FastAPI service, interactive command-line search tools, and JSONL batch exporters.

The project is built around a small shared contract:

- retailer-specific clients handle store lookup, session setup, search, and parsing
- products and store locations are normalized through Pydantic models in `app/models.py`
- Redis-backed caches reduce repeat store and product fetches when Redis is available
- the matching service scores candidate products across retailers as equivalents, substitutes, or different items

## Supported Retailers

| Retailer | Store lookup | Product search | Batch export | Notes |
| --- | --- | --- | --- | --- |
| ALDI | Yes | Yes | Yes | Uses Instacart-backed GraphQL flows and ZIP-specific inventory context. |
| Kroger | Yes | Yes | Yes | Uses Kroger store APIs plus browser-backed product search paths. |
| Publix | Yes | Yes | Yes | Uses a fast fetch path with a stealth browser fallback. |
| Walmart | Yes | Yes | Yes | Uses store-location cookies for store-scoped search results. |

## Requirements

- Python 3.12
- `uv`
- Playwright browser dependencies for browser-backed scraper paths
- Redis, optional, for cross-process caching

Install dependencies:

```bash
uv sync
```

Install a Chromium browser for Playwright-backed flows:

```bash
uv run playwright install chromium
```

Redis is optional. If it is unavailable, the app skips cache reads and writes and continues with live fetches. To point the app at Redis:

```bash
export REDIS_HOST=localhost
export REDIS_PORT=6379
```

## Run The API

```bash
uv run start-api
```

By default the API listens on `0.0.0.0:8000`.

```bash
export API_HOST=127.0.0.1
export API_PORT=8000
uv run start-api
```

Useful endpoints:

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Basic service health check. |
| `GET` | `/api/v1/{retailer}/locations?zip_code=30303` | Find nearby stores for `aldi`, `kroger`, `publix`, or `walmart`. |
| `GET` | `/api/v1/{retailer}/search?q=milk&location_id=123` | Search one retailer, optionally scoped to a store. |
| `GET` | `/api/v1/search?q=milk` | Search all retailers and return the top result from each. |
| `POST` | `/api/v1/match/search` | Search retailers and score candidate products for equivalence. |

Example matching request:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/match/search \
  -H 'content-type: application/json' \
  -d '{
    "query": "2% milk 1 gallon",
    "retailers": ["walmart", "kroger"],
    "location_ids": {
      "walmart": "789",
      "kroger": "123"
    },
    "zip_code": "30303",
    "max_candidates_per_retailer": 3
  }'
```

Swagger UI is available at `http://127.0.0.1:8000/docs` when the API is running locally.

## Interactive Search

Each retailer has an interactive command that prompts for a query and, optionally, a store selection:

```bash
uv run aldi-search
uv run kroger-search
uv run publix-search
uv run walmart-search
```

The interactive flow can:

1. search using the retailer default context
2. ask for a ZIP code
3. list nearby stores
4. build retailer-specific cookies or inventory context
5. display normalized product results

## Batch Exports

Batch exporters run the shared grocery query set from `app/common_queries.py` and write JSONL output.

```bash
uv run aldi-batch --zip-code 30303 --location-id 123 --max-results 10 --output aldi_products.jsonl
uv run kroger-batch --location-id 123 --max-results 10 --output kroger_products.jsonl
uv run publix-batch --location-id 123 --max-results 10 --output publix_products.jsonl
uv run walmart-batch
```

`walmart-batch` currently uses the default store and ZIP configured in `app/walmart/export.py`.

## Product Matching

The matching layer converts queries and product records into normalized fingerprints, then scores candidates with brand, size, category, token, and attribute rules.

Results are grouped into:

- `equivalent`: strong matches for the requested product
- `substitutes`: plausible alternatives that are not exact equivalents
- `rejected`: candidates that do not clear the matching rules

Retailer errors are returned in the response `errors` object instead of failing the whole matching request.

## Project Layout

```text
app/
  api/              FastAPI app, routers, dependencies, and exception handlers
  aldi/             ALDI client, parser, spider, constants, and exporter
  kroger/           Kroger client, parser, spider, browser pool, and exporter
  matching/         Product fingerprinting and equivalence scoring
  publix/           Publix client, parser, spider, constants, and exporter
  utils/            Fetching, store selection, caches, ZIP lookup, and display helpers
  walmart/          Walmart client, parser, spider, cookies, constants, and exporter
tests/
  unit/             Parser, cache, matching, model, and retailer unit tests
  integration/      Live or integration-style scraper tests
  performance/      Latency regression and baseline tests
```

## Testing

Run the full test suite:

```bash
uv run pytest
```

Run only unit tests:

```bash
uv run pytest tests/unit
```

Run performance tests:

```bash
uv run pytest -m perf
```

Some scraper behavior depends on live third-party websites. Network availability, retailer markup changes, anti-bot systems, and store inventory changes can affect live integration results even when the local code is unchanged.

## Development Notes

- Normalized output should pass through `normalize_product` or `normalize_location`.
- Store and product cache keys are retailer-scoped to avoid cross-retailer collisions.
- Browser-backed paths should be treated as slower fallbacks unless a retailer requires them.
- Generated JSONL output belongs under each retailer's `spider_results/` directory or a caller-provided output path.
- Keep retailer-specific parsing in each retailer package and shared behavior in `app/utils` or `app/matching`.
