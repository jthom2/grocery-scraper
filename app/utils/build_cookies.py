import uuid
import orjson
import base64
import time
from urllib.parse import quote

# builds cookies for a specific store
def build_location_cookies(store_id, zip_code):
    acid = str(uuid.uuid4())
    timestamp_ms = int(time.time() * 1000)

    # core payload shared by locGuestData and locDataV3
    payload = {
        "intent": "SHIPPING",
        "storeIntent": "PICKUP",
        "mergeFlag": True,
        "pickup": {
            "nodeId": str(store_id),
            "timestamp": timestamp_ms,
        },
        "postalCode": {
            "base": str(zip_code),
            "timestamp": timestamp_ms,
        },
        "validateKey": f"prod:v2:{acid}",
    }

    # serialize → base64 → URL-encode (Walmart's cookie format)
    json_str = orjson.dumps(payload).decode()
    b64 = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")
    encoded = quote(b64, safe="")

    return {
        "ACID": acid,
        "hasACID": "true",
        "hasLocData": "1",
        "assortmentStoreId": str(store_id),
        "locGuestData": encoded,
        "locDataV3": encoded,
    }
