import sys
import re
import json
from pathlib import Path

project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
##################################################################
from app.utils import fetcher
from app.kroger import locate_store, search_products



zip_code = input("ZIP: ")
stores = locate_store.get_stores(zip_code)
locate_store.display_stores(stores, zip_code)
selected = locate_store.select_store(stores)
store_id = selected['location_id']



cookies = {
    "DD_modStore": store_id,
    "x-active-modality": (
        '{"type":"IN_STORE",'
        f'"locationId":"{store_id}",'
        '"source":"MODALITY_OPTIONS",'
        '"createdDate":1775710908718}'
    ),
}




query = input("Search Kroger for: ")
results = search_products.search(query, cookies)
search_products.display_results(results, query)