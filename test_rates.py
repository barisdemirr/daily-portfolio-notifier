from rates import get_all_rates

if __name__ == "__main__":
    rates = get_all_rates()
    for asset, price in rates.items():
        print(f"{asset}: {price}")