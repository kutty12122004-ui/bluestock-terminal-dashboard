# Bluestock Terminal Dashboard

A Django-based financial intelligence dashboard for corporate data ingestion, sectoral classification, and dynamic market analytics.

---

## Features

- **Market Matrix** — Listed asset index with keyword search and filtering
- **Sectoral Breakdown** — Auto-clusters assets by industry segment (Retail, Technology, Healthcare, etc.)
- **8-Chart Engine** — Deterministic financial charts per company: Revenue, Net Profit Margin, Debt-to-Equity, ROCE, Shareholding, and Valuations via Chart.js
- **Market Screener** — Cross-sectional screening by financial ratios (Max D/E, Min NPM, etc.)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django (Python) |
| Database | PostgreSQL |
| Frontend | HTML5, Vanilla JS, Tailwind CSS |
| Charts | Chart.js (CDN) |
| Data Utilities | Python CSV, Hashlib |

---

## Local Setup

**Prerequisites:** Python 3.11+, PostgreSQL, Git

```bash
# 1. Clone and enter the project
git clone https://github.com/kutty12122004-ui/bluestock-terminal-dashboard.git
cd bluestock-terminal-dashboard

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 3. Configure .env with your DB credentials (do not commit)

# 4. Run migrations
python manage.py migrate

# 5. Import company data
python manage.py import_companies dim_company.csv

# 6. Start the server
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

---

## Project Structure

```
bluestock-terminal-dashboard/
├── accounts/          # Auth
├── api_management/    # API layer
├── bluestock_core/    # Core settings
├── companies/         # Company models & views
├── dashboard/         # Dashboard UI
├── etl/               # Data ingestion
├── ml_engine/         # Analytics engine
├── dim_company.csv    # Source data
└── manage.py
```
