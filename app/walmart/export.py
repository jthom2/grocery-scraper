import json
import logging
import os
from app.common_queries import COMMON_GROCERY_SEARCHES
from app.walmart.spider import run_walmart_batch

# configure logging to see progress
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    queries = list(COMMON_GROCERY_SEARCHES)
    location_id = "4673"
    zip_code = "36830"
    
    # ensure results directory exists
    output_dir = os.path.join(os.path.dirname(__file__), "spider_results")
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, "walmart_products.jsonl")
    
    print(f"Starting Walmart batch search for: {', '.join(queries)}")
    print(f"Store: {location_id} | Zip: {zip_code}")
    
    try:
        results = run_walmart_batch(
            queries=queries,
            location_id=location_id,
            zip_code=zip_code,
            max_results=10 # items per query
        )
        
        print(f"\nFound {len(results)} total items.")
        print(f"Saving to {filename}...")
        
        with open(filename, "w", encoding="utf-8") as f:
            for item in results:
                f.write(json.dumps(item) + "\n")
                
        print(f"Success! You can now view the output in {filename}")
        
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
