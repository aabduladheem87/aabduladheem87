#!/usr/bin/env python3
"""Generate renewal reminders and email drafts for insurance broker policies."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterable, List

DATE_FORMAT = "%Y-%m-%d"


@dataclass(frozen=True)
class Policy:
    policy_id: str
    client_name: str
    client_email: str
    renewal_date: date
    premium: float


@dataclass(frozen=True)
class Reminder:
    policy: Policy
    days_until_renewal: int


def parse_policy(row: dict) -> Policy:
    return Policy(
        policy_id=row["policy_id"].strip(),
        client_name=row["client_name"].strip(),
        client_email=row["client_email"].strip(),
        renewal_date=datetime.strptime(row["renewal_date"].strip(), DATE_FORMAT).date(),
        premium=float(row["premium"].strip()),
    )


def load_policies(csv_path: Path) -> List[Policy]:
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"policy_id", "client_name", "client_email", "renewal_date", "premium"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")
        return [parse_policy(row) for row in reader]


def build_reminders(policies: Iterable[Policy], window_days: int, as_of: date) -> List[Reminder]:
    reminders: List[Reminder] = []
    window_end = as_of + timedelta(days=window_days)
    for policy in policies:
        if as_of <= policy.renewal_date <= window_end:
            reminders.append(
                Reminder(
                    policy=policy,
                    days_until_renewal=(policy.renewal_date - as_of).days,
                )
            )
    return sorted(reminders, key=lambda reminder: reminder.days_until_renewal)


def build_email(reminder: Reminder) -> str:
    policy = reminder.policy
    return (
        f"Subject: Upcoming renewal for policy {policy.policy_id}\n\n"
        f"Hi {policy.client_name},\n\n"
        f"Your policy {policy.policy_id} is set to renew on {policy.renewal_date:%B %d, %Y} "
        f"(in {reminder.days_until_renewal} days). "
        "Reply to confirm any updates, coverage changes, or documentation we should review ahead of renewal.\n\n"
        "Thanks,\n"
        "Your Insurance Brokerage Team\n"
    )


def write_emails(reminders: Iterable[Reminder], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for reminder in reminders:
        policy = reminder.policy
        filename = output_dir / f"{policy.policy_id}_{policy.client_name.replace(' ', '_')}.txt"
        filename.write_text(build_email(reminder), encoding="utf-8")


def format_summary(reminders: Iterable[Reminder]) -> str:
    lines = ["Renewal reminders:" ]
    for reminder in reminders:
        policy = reminder.policy
        lines.append(
            f"- {policy.policy_id}: {policy.client_name} | {policy.renewal_date:%Y-%m-%d} "
            f"({reminder.days_until_renewal} days) | ${policy.premium:,.2f}"
        )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate renewal reminders and email drafts from a policy CSV."
    )
    parser.add_argument("csv", type=Path, help="Path to the policy CSV file.")
    parser.add_argument(
        "--window-days",
        type=int,
        default=30,
        help="Number of days ahead to include renewals.",
    )
    parser.add_argument(
        "--as-of",
        type=str,
        default=date.today().strftime(DATE_FORMAT),
        help="Date to treat as 'today' in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs"),
        help="Directory to store generated email drafts.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    as_of = datetime.strptime(args.as_of, DATE_FORMAT).date()
    policies = load_policies(args.csv)
    reminders = build_reminders(policies, args.window_days, as_of)
    if not reminders:
        print("No renewals found within the window.")
        return

    print(format_summary(reminders))
    write_emails(reminders, args.output_dir)
    print(f"\nDraft emails saved to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
