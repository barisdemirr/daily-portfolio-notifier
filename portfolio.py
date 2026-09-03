import json
import sys
import os

PORTFOLIO_FILE = os.path.join(os.path.dirname(__file__), "portfolio.json")
VALID_ASSETS = ["USD", "EUR", "GRAM_ALTIN", "CEYREK_ALTIN", "YARIM_ALTIN", "TAM_ALTIN"]


def load_portfolio():
    if not os.path.exists(PORTFOLIO_FILE):
        return {asset: 0 for asset in VALID_ASSETS}
    with open(PORTFOLIO_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    for asset in VALID_ASSETS:
        data.setdefault(asset, 0)
    return data


def save_portfolio(data):
    with open(PORTFOLIO_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_asset(asset, amount):
    data = load_portfolio()
    data[asset] = data.get(asset, 0) + amount
    save_portfolio(data)
    print(f"{asset}: {data[asset]}")


def set_asset(asset, amount):
    data = load_portfolio()
    data[asset] = amount
    save_portfolio(data)
    print(f"{asset}: {data[asset]}")


def list_portfolio():
    data = load_portfolio()
    for asset, amount in data.items():
        print(f"{asset}: {amount}")


def print_usage():
    print("usage:")
    print("  python portfolio.py list")
    print("  python portfolio.py add <ASSET> <AMOUNT>")
    print("  python portfolio.py set <ASSET> <AMOUNT>")
    print(f"valid assets: {', '.join(VALID_ASSETS)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        list_portfolio()
    elif command in ("add", "set"):
        if len(sys.argv) != 4:
            print_usage()
            sys.exit(1)
        asset = sys.argv[2].upper()
        if asset not in VALID_ASSETS:
            print(f"invalid asset: {asset}")
            print(f"valid assets: {', '.join(VALID_ASSETS)}")
            sys.exit(1)
        try:
            amount = float(sys.argv[3])
        except ValueError:
            print("amount must be a number")
            sys.exit(1)
        if command == "add":
            add_asset(asset, amount)
        else:
            set_asset(asset, amount)
    else:
        print_usage()
        sys.exit(1)
