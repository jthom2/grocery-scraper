import pytest
from unittest.mock import MagicMock, patch
import orjson
import redis
from app.utils.product_cache import ProductCache


@pytest.fixture
def mock_redis():
    with patch("redis.Redis") as mock:
        yield mock


def test_cache_key_generation():
    cache = ProductCache()
    key1 = cache._get_key("walmart", "123", "milk")
    key2 = cache._get_key("walmart", "123", " MILK ")
    assert key1 == "products:walmart:123:milk"
    assert key1 == key2


def test_cache_get_hit(mock_redis):
    # setup mock client
    mock_client = MagicMock()
    mock_redis.return_value = mock_client
    
    products = [{"name": "Milk", "price": 4.99}]
    mock_client.get.return_value = orjson.dumps(products)
    
    cache = ProductCache()
    result = cache.get("walmart", "123", "milk")
    
    assert result == products
    mock_client.get.assert_called_once_with("products:walmart:123:milk")


def test_cache_get_miss(mock_redis):
    mock_client = MagicMock()
    mock_redis.return_value = mock_client
    mock_client.get.return_value = None
    
    cache = ProductCache()
    result = cache.get("walmart", "123", "milk")
    
    assert result is None


def test_cache_set(mock_redis):
    mock_client = MagicMock()
    mock_redis.return_value = mock_client
    
    cache = ProductCache()
    products = [{"name": "Milk", "price": 4.99}]
    cache.set("walmart", "123", "milk", products, ttl_hours=1)
    
    mock_client.setex.assert_called_once()
    args, _ = mock_client.setex.call_args
    assert args[0] == "products:walmart:123:milk"
    assert args[1] == 3600  # 1 hour in seconds
    assert orjson.loads(args[2]) == products


def test_graceful_degradation_on_connection_error(mock_redis):
    # simulate redis being down
    mock_redis.return_value.ping.side_effect = redis.ConnectionError("Connection refused")
    
    cache = ProductCache()
    # first call tries to connect and fails
    result = cache.get("walmart", "123", "milk")
    
    assert result is None
    assert cache._is_available is False
    
    # second call should return None immediately without trying to connect again
    result2 = cache.get("walmart", "123", "milk")
    assert result2 is None
    assert mock_redis.call_count == 1  # only one attempt
