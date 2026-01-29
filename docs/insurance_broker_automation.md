# Insurance Broker Automation Idea

## Most time-consuming repetitive task (industry generalization)

Insurance brokers consistently spend significant time on **renewal follow-ups and data re-entry**. The work typically includes:

- Manually tracking renewal dates across many policies.
- Following up with clients to confirm changes and gather updated documents.
- Drafting renewal reminder emails.
- Re-entering identical policy data into multiple carrier portals.

This mix of tracking, chasing, and re-keying data is high-volume and time-sensitive, which makes it a prime automation target.

## Proposed automation app

Create a lightweight **Renewal Reminder Automation** app that:

1. Ingests a CSV export of policies.
2. Flags policies renewing within a configurable window (e.g., 30 days).
3. Generates a prioritized reminder list.
4. Produces draft client email templates for brokers to review and send.

The initial version in this repo covers steps 1–4 and provides a foundation for expansion (e.g., CRM integration, carrier submissions, and document collection workflows).
