import os
import requests

RAPIDAPI_HOST = "doviz-ve-altin-fiyatlari-try.p.rapidapi.com"
CURRENCY_URL = f"https://{RAPIDAPI_HOST}/doviz"
GOLD_URL = f"https://{RAPIDAPI_HOST}/altin"


def _headers():
    api_key = os.environ.get("RAPIDAPI_KEY")
    if not api_key:
        raise RuntimeError("RAPIDAPI_KEY environment variable is not set")
    return {
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": api_key,
    }


def _find_item(items, keywords):
    for item in items:
        name = str(item.get("name", "")).lower()
        if all(k in name for k in keywords):
            return item
    return None


def get_currency_rates():
    response = requests.get(CURRENCY_URL, headers=_headers(), timeout=10)
    response.raise_for_status()
    data = response.json().get("result", [])

    usd = _find_item(data, ["dolar"])
    eur = _find_item(data, ["euro"])

    if usd is None or eur is None:
        raise RuntimeError("could not locate USD or EUR in currency response")

    return {
        "USD": float(usd["selling"]),
        "EUR": float(eur["selling"]),
    }


def get_gold_prices():
    response = requests.get(GOLD_URL, headers=_headers(), timeout=10)
    response.raise_for_status()
    data = response.json().get("result", [])

    gram = _find_item(data, ["gram"])
    ceyrek = _find_item(data, ["çeyrek"])
    yarim = _find_item(data, ["yarım"])
    tam = _find_item(data, ["tam"])

    if not all([gram, ceyrek, yarim, tam]):
        raise RuntimeError("could not locate all gold types in gold response")

    return {
        "GRAM_ALTIN": float(gram["selling"]),
        "CEYREK_ALTIN": float(ceyrek["selling"]),
        "YARIM_ALTIN": float(yarim["selling"]),
        "TAM_ALTIN": float(tam["selling"]),
    }


def get_all_rates():
    rates = {}
    rates.update(get_currency_rates())
    rates.update(get_gold_prices())
    return rates
