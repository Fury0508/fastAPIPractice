import httpx
from service.cache import get_cache, set_cache
from datetime import datetime
async def fetch_currency(
    base_currency: str) -> dict[str, float]:
    """
    Fetches the exchange rate from base_currency to target_currency using the ExchangeRate-API.
    Caches the result for 1 hour to reduce API calls.

    Returns the exchange rate as a float.
    Raises an exception if the API call fails or if the currencies are invalid.
    """
    cache_key = f"currency_{base_currency}"
    cached_rate = get_cache(cache_key)
    if cached_rate is not None:
        return cached_rate

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://v6.exchangerate-api.com/v6/7c808a35a1c9362c76bd9c62/latest/{base_currency.upper()}"
        )
        response.raise_for_status()
        data = response.json()
    
        exchange_rate = data.get("conversion_rates", {})
        set_cache(cache_key, exchange_rate, ttl=3600)
        return exchange_rate