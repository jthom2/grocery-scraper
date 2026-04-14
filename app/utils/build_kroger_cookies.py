import orjson
import time


def build_location_cookies(store_id):
    timestamp_ms = int(time.time() * 1000)

    return {
        "DD_modStore": store_id,
        "x-active-modality": orjson.dumps({
            "type": "IN_STORE",
            "locationId": store_id,
            "source": "MODALITY_OPTIONS",
            "createdDate": timestamp_ms
        }).decode()
    }
