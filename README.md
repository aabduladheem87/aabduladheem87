# Insurance Broker Renewal Automation

This repo contains a small automation starter app focused on one of the most time-consuming, repetitive tasks in insurance brokerage operations: renewal follow-ups and data re-entry.

## Why this task?

Renewal management is a constant, high-volume workload. Brokers spend time tracking renewal dates, chasing updates, and drafting reminders across many policies. Automating reminders and drafting emails reduces manual effort and frees time for advisory work. For details, see the full write-up: [docs/insurance_broker_automation.md](docs/insurance_broker_automation.md).

## What the app does

- Reads a policy CSV export.
- Identifies policies renewing within a configurable window.
- Prints a prioritized reminder list.
- Generates draft reminder emails for each client.

## Quick start

```bash
python3 app/renewal_reminder.py data/sample_policies.csv --window-days 30 --as-of 2025-01-15
```

Draft emails will be created in the `outputs/` directory.

## CSV format

The app expects these columns:

- `policy_id`
- `client_name`
- `client_email`
- `renewal_date` (YYYY-MM-DD)
- `premium`
