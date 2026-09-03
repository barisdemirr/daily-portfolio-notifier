# Kur Takip 💰📈

**A tiny robot that watches your money so you don't have to.**

Every day at 18:00 (Turkey time), this project quietly wakes up on
GitHub's servers, checks the current USD, EUR, and gold prices (gram,
quarter, half, full), multiplies them against your actual holdings,
compares the result to yesterday's number, and emails you a one-line
verdict: **richer or poorer, and by how much.** Then it goes back to
sleep until tomorrow.

No dashboard to open. No app to check. No manual math after doom-scrolling
exchange rate headlines. It just lands in your inbox, unprompted, at the
same time every day — currently in active daily use, running fully
unattended via GitHub Actions.

## What it actually does

- 📊 Tracks your portfolio (USD, EUR, gram/quarter/half/full gold) in a
  simple JSON file — no database, no accounts, no nonsense
- 🌐 Pulls live sell prices from a currency/gold API
- 💌 Emails you a report via Gmail, summary first — no "click to expand"
  required, the verdict is right there in the notification
- 📉📈 Remembers yesterday's total and tells you exactly how many TL you
  gained or lost since then
- 🙈 Skips any asset you're not holding (zero balances don't clutter
  the report)
- 🤖 Runs itself every day at 18:00 TR time via GitHub Actions —
  set it up once, forget it exists, let it work

## Setup

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Configure your secrets

Create a `.env` file in the project folder (use `.env.example` as a
template):

```
RAPIDAPI_KEY=...
GMAIL_ADDRESS=...
GMAIL_APP_PASSWORD=...
MAIL_RECIPIENT=...
```

- `RAPIDAPI_KEY` — your key for the "Döviz ve Altın Fiyatları (TRY)" API on RapidAPI
- `GMAIL_ADDRESS` — the Gmail account sending the report
- `GMAIL_APP_PASSWORD` — a Gmail App Password (not your regular password)
- `MAIL_RECIPIENT` — where the report goes (defaults to `GMAIL_ADDRESS` if left empty)

To get a Gmail App Password: Google Account > Security > enable
2-Step Verification > App Passwords > generate a new one. It must be
created for the same account as `GMAIL_ADDRESS`.

`.env` is listed in `.gitignore`, so it never gets pushed to the repo.

### 3. Set up your portfolio

```
python portfolio.py add USD 100
python portfolio.py add EUR 50
python portfolio.py set CEYREK_ALTIN 3
python portfolio.py list
```

Valid assets: `USD`, `EUR`, `GRAM_ALTIN`, `CEYREK_ALTIN`, `YARIM_ALTIN`, `TAM_ALTIN`

These commands create/update `portfolio.json`. It's also gitignored —
your holdings never leave your machine unless you put them in a
GitHub secret yourself (see below).

### 4. Run it manually

```
python main.py
```

Prints the report to the terminal and sends it by email. The total
from this run is saved to `history.json`, so the next run can tell
you whether you gained or lost money since then. (First run won't
show a profit/loss line — there's nothing to compare yet.)

## Running it automatically with GitHub Actions

`.github/workflows/daily-report.yml` is scheduled to run every day at
UTC 15:00 (18:00 Turkey time). Change the `cron` value in that file if
you want a different time (it's UTC-based, so do the math).

To let GitHub Actions run this for you, add these repo secrets
(Settings > Secrets and variables > Actions):

- `RAPIDAPI_KEY`
- `GMAIL_ADDRESS`
- `GMAIL_APP_PASSWORD`
- `MAIL_RECIPIENT`
- `PORTFOLIO_JSON` — the full content of your local `portfolio.json`, as one JSON blob

To create `PORTFOLIO_JSON`, just copy the contents of your local
`portfolio.json` and paste them in as the secret value. If your
holdings change later, update this secret manually.

After each run, the workflow automatically commits the updated
`history.json` back to the repo — that's how tomorrow's run knows
what today's number was.

Want to test it without waiting for 18:00? Go to repo > Actions >
"daily-report" > "Run workflow".