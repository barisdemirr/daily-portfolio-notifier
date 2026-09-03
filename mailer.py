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


def build_report(portfolio, rates):
    lines = []
    total = 0.0

    for asset, amount in portfolio.items():
        price = rates.get(asset)
        if price is None:
            continue
        value = amount * price
        total += value
        label = ASSET_LABELS.get(asset, asset)
        lines.append(f"{label}: {amount} x {price:.2f} TL = {value:.2f} TL")

    lines.append("")
    lines.append(f"Toplam Portföy Değeri: {total:.2f} TL")
    return "\n".join(lines)


def send_email(subject, body):
    sender = os.environ.get("GMAIL_ADDRESS")
    password = os.environ.get("GMAIL_APP_PASSWORD")
    recipient = os.environ.get("MAIL_RECIPIENT", sender)

    if not sender or not password:
        raise RuntimeError("GMAIL_ADDRESS or GMAIL_APP_PASSWORD environment variable is not set")

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, [recipient], msg.as_string())
