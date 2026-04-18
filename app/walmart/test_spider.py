import logging
from app.walmart.spider import WalmartSpider, run_walmart_batch

def main():
    logging.basicConfig(level=logging.INFO)
    queries = ["milk", "eggs", "bread"]
    location_id = "5438" # specific store id
    zip_code = "72712"
    
    print("Starting spider batch run...")
    results = run_walmart_batch(queries, location_id, zip_code, max_results=3)
    for item in results:
        print(f"Found product for '{item.get('query')}': {item.get('name')}")

if __name__ == "__main__":
    main()
