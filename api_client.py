import requests
import os
from config import EXCHANGE_RATE_API_KEY


def get_current_rate(default: str = "USD", currencies: list[str] = ["EUR", "GBP", "JPY"]):
    """
    Get current exchange rates from exchangerate.host API
    """
    url = "https://api.exchangerate.host/live"
    params = {
        "access_key": EXCHANGE_RATE_API_KEY,
        "source": default,
        "currencies": ",".join(currencies)
        # ",".join(currencies) означает объединение в строку с разделителем-запятой
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return {"success": False, "error": {"info": str(e)}}


def convert_currency(amount, from_currency, to_currency):
    """
    Convert currency using exchangerate.host API
    """
    url = "https://api.exchangerate.host/convert"
    params = {
        "access_key": EXCHANGE_RATE_API_KEY,
        "from": from_currency,
        "to": to_currency,
        "amount": amount
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error converting currency: {e}")
        return {"success": False, "error": {"info": str(e)}}


def get_historical_rate(date, from_currency, to_currency):
    """
    Get historical exchange rate for a specific date
    """
    url = f"https://api.exchangerate.host/{date}"
    params = {
        "access_key": EXCHANGE_RATE_API_KEY,
        "base": from_currency,
        "symbols": to_currency
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching historical rate: {e}")
        return {"success": False, "error": {"info": str(e)}}


if __name__ == "__main__":
    data = get_current_rate(default="RUB", currencies=["USD", "EUR", "GBP", "JPY", "CNY"])
    
    if data.get("success"):
        print(data["quotes"])
    else:
        error_info = data.get("error", {}).get("info", "Unknown error")
        print(f"API Error: {error_info}")
        print("Please make sure you have specified the correct 'access_key' in the function get_current_rate.")

    print(convert_currency(100, "RUB", "USD"))