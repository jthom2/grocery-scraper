from app.aldi.client import AldiClient
from app.kroger.client import KrogerClient
from app.publix.client import PublixClient
from app.walmart.client import WalmartClient


def get_aldi_client() -> AldiClient:
    return AldiClient()


def get_kroger_client() -> KrogerClient:
    return KrogerClient()


def get_publix_client() -> PublixClient:
    return PublixClient()


def get_walmart_client() -> WalmartClient:
    return WalmartClient()
