import pytest
from unittest.mock import MagicMock, patch
import orjson
import redis
from app.utils.store_cache import StoreCache


@pytest.fixture
def mock_redis():
    with patch("redis.Redis") as mock:
        yield mock


def test_store_cache_key_generation():
    cache = StoreCache()
    key1 = cache._get_key("walmart", "30303")
    key2 = cache._get_key("walmart", " 30303 ")
    assert key1 == "stores:walmart:30303"
    assert key1 == key2


def test_store_cache_get_hit(mock_redis):
    # setup mock client
    mock_client = MagicMock()
    mock_redis.return_value = mock_client
    
    stores = [{"name": "Walmart Supercenter", "location_id": "123"}]
    mock_client.get.return_value = orjson.dumps(stores)
    
    cache = StoreCache()
    result = cache.get("walmart", "30303")
    
    assert result == stores
    mock_client.get.assert_called_once_with("stores:walmart:30303")


def test_store_cache_get_miss(mock_redis):
    mock_client = MagicMock()
    mock_redis.return_value = mock_client
    mock_client.get.return_value = None
    
    cache = StoreCache()
    result = cache.get("walmart", "30303")
    
    assert result is None


def test_store_cache_set(mock_redis):
    mock_client = MagicMock()
    mock_redis.return_value = mock_client
    
    cache = StoreCache()
    stores = [{"name": "Walmart Supercenter", "location_id": "123"}]
    cache.set("walmart", "30303", stores, ttl_hours=1)
    
    mock_client.setex.assert_called_once()
    args, _ = mock_client.setex.call_args
    assert args[0] == "stores:walmart:30303"
    assert args[1] == 3600  # 1 hour in seconds
    assert orjson.loads(args[2]) == stores


def test_store_cache_graceful_degradation_on_connection_error(mock_redis):
    # simulate redis being down
    mock_redis.return_value.ping.side_effect = redis.ConnectionError("Connection refused")
    
    cache = StoreCache()
    # first call tries to connect and fails
    result = cache.get("walmart", "30303")
    
    assert result is None
    assert cache._is_available is False
    
    # second call should return None immediately without trying to connect again
    result2 = cache.get("walmart", "30303")
    assert result2 is None
    assert mock_redis.call_count == 1  # only one attempt
