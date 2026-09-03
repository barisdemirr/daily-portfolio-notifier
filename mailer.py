import os
import smtplib
from email.mime.text import MIMEText

ASSET_LABELS = {
    "USD": "Dolar",
    "EUR": "Euro",
    "GRAM_ALTIN": "Gram Altın",
    "CEYREK_ALTIN": "Çeyrek Altın",
    "YARIM_ALTIN": "Yarım Altın",
    "TAM_ALTIN": "Tam Altın",
}


def calculate_total(portfolio, rates):
    total = 0.0
    for asset, amount in portfolio.items():
        price = rates.get(asset)
        if price is None:
            continue
        total += amount * price
    return total


def build_report(portfolio, rates, previous_total=None):
    total = calculate_total(portfolio, rates)

    summary_lines = [f"Satarsan Eline Geçecek Toplam: {total:.2f} TL"]

    if previous_total is not None:
        diff = total - previous_total
        durum = "Kâr" if diff >= 0 else "Zarar"
        summary_lines.append(f"Dünden Bugüne {durum}: {diff:+.2f} TL")

    detail_lines = []
    for asset, amount in portfolio.items():
        if amount == 0:
            continue
        price = rates.get(asset)
        if price is None:
            continue
        value = amount * price
        label = ASSET_LABELS.get(asset, asset)
        detail_lines.append(f"{label}: {amount} x {price:.2f} TL = {value:.2f} TL")

    lines = summary_lines + [""] + detail_lines
    return "\n".join(lines)


def send_email(subject, body):
    sender = os.environ.get("GMAIL_ADDRESS")
    password = os.environ.get("GMAIL_APP_PASSWORD")
    recipient = os.environ.get("MAIL_RECIPIENT", sender)

    if not sender or not password:
        raise RuntimeError("GMAIL_ADDRESS or GMAIL_APP_PASSWORD environment variable is not set")

    print(f"sending from={sender} to={recipient} password_length={len(password)}")

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.set_debuglevel(1)
        server.login(sender, password)
        server.sendmail(sender, [recipient], msg.as_string())
    print("send_email finished without raising")