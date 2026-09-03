from datetime import date

from dotenv import load_dotenv

load_dotenv()

from portfolio import load_portfolio
from rates import get_all_rates
from mailer import build_report, calculate_total, send_email
from history import load_previous_total, save_total


def main():
    portfolio = load_portfolio()
    rates = get_all_rates()

    previous_total = load_previous_total()
    report = build_report(portfolio, rates, previous_total)

    subject = f"Portföy Raporu - {date.today().isoformat()}"
    send_email(subject, report)
    print(report)

    current_total = calculate_total(portfolio, rates)
    save_total(current_total)


if __name__ == "__main__":
    main()