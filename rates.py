import os
import requests

RAPIDAPI_HOST = "doviz-ve-altin-fiyatlari-try.p.rapidapi.com"
BASE_URL = f"https://{RAPIDAPI_HOST}/economy/currency/exchange-rate"

ASSET_CODES = {
    "USD": "USD",
    "EUR": "EUR",
    "GRAM_ALTIN": "gram-altin",
    "CEYREK_ALTIN": "ceyrek-altin",
    "YARIM_ALTIN": "yarim-altin",
    "TAM_ALTIN": "tam-altin",
}


def _headers():
    api_key = os.environ.get("RAPIDAPI_KEY")
    if not api_key:
        raise RuntimeError("RAPIDAPI_KEY environment variable is not set")
    return {
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": api_key,
    }


def _fetch(codes, extra_params=None):
    params = {"code": ",".join(codes)}
    if extra_params:
        params.update(extra_params)
    response = requests.get(BASE_URL, headers=_headers(), params=params, timeout=10)
    response.raise_for_status()
    payload = response.json()
    if payload.get("status") != "success":
        raise RuntimeError(f"API returned non-success status: {payload}")
    return payload.get("data", [])


def _index_by_code(items):
    return {item["code"]: item for item in items}


def get_all_rates():
    codes = list(ASSET_CODES.values())
    items = _fetch(codes)
    by_code = _index_by_code(items)

    if len(by_code) < len(codes):
        missing = [c for c in codes if c not in by_code]
        raise RuntimeError(f"missing codes in response: {missing}")

    return {
        asset: float(by_code[code]["selling"])
        for asset, code in ASSET_CODES.items()
    }