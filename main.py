from datetime import date

from portfolio import load_portfolio
from rates import get_all_rates
from mailer import build_report, send_email


def main():
    portfolio = load_portfolio()
    rates = get_all_rates()
    report = build_report(portfolio, rates)
    subject = f"Portföy Raporu - {date.today().isoformat()}"
    send_email(subject, report)
    print(report)


if __name__ == "__main__":
    main()
