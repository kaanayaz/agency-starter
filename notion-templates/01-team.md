# Team

Single source of truth for who's on the agency. Every agent ping, approval routing, and Slack mention pulls from here. Keep it current — bad routing is the #1 cause of "my agent ignored me" complaints.

## Schema

| Property | Type | Options | Required | Notes |
|---|---|---|---|---|
| Name | Title | — | yes | Display name |
| Role | Select | Founder, Account Manager, Producer, Designer, Finance, Developer, Operator | yes | Loose buckets, not job titles |
| Email | Email | — | yes | Used for Gmail draft routing |
| Slack User ID | Text | — | yes | Starts with `U`. In Slack: right-click profile → `•••` → Copy member ID. Without this, agents can't `<@mention>` |
| Working Hours | Text | — | yes | Format: `Mon-Fri 09:00-18:00`. Use 24h. Timezone goes in the next field |
| Primary Timezone | Text | — | yes | IANA name (e.g. `Europe/Istanbul`). The first row's value is the agency-wide default the Orchestrator falls back to |
| Preferred Language | Text | — | yes | Two-letter code (e.g. `tr`, `en`, `es`) or full name (`Turkish`). The Orchestrator and any agent dispatched on this person's behalf reads this and replies in that language. First row's value is the agency-wide system-language default; per-content-language override lives in Brand Voice |
| Default Owner For | Multi-select | invoices, decks, finance, outreach, contracts, design, dev, scheduling, reports | no | Used by agents to pick a default human owner when none is named on a Todo |
| Approval Tier | Select | auto-approve, light-review, always-review, page-on-issue | yes | Drives how aggressively agents wait for this person before acting |
| On-Call | Checkbox | — | no | Critical alerts (data risk, prod down) page everyone with this checked, regardless of working hours |
| Status | Select | active, archived | yes | Don't delete people who leave; set archived. Past Run Log entries reference these rows |

## Seed rows

Replace during discovery. Three placeholders so you can see the shape:

| Name | Role | Email | Slack User ID | Working Hours | Primary Timezone | Preferred Language | Default Owner For | Approval Tier | On-Call | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| Bugra Kaan Ayaz | Founder | bugra@foundby.me | U00000000 | Mon-Sun 09:00-22:00 | Europe/Istanbul | tr | invoices, finance, dev | always-review | yes | active |
| (Account lead) | Account Manager | — | — | Mon-Fri 09:00-18:00 | Europe/Istanbul | tr | outreach, decks, contracts | light-review | no | active |
| (Producer) | Producer | — | — | Mon-Fri 10:00-19:00 | Europe/Istanbul | tr | scheduling, reports | light-review | no | active |

## Read/write contract

- **Reads:** Orchestrator (every run); every dispatched agent (when picking an owner)
- **Writes:** humans only — agents never edit Team
- **Change rate:** monthly at most (joiners, leavers, role changes)

## Setup pitfalls

- **Slack User ID format**: must start with `U`. The visible handle (`@bugra`) won't work in API calls.
- **First row sets the agency-wide default timezone.** If row 1's `Primary Timezone` is wrong, every Run Log entry is off by hours.
- **Working Hours has no timezone in it** — that's the next field. Mixing them produces ambiguous parses.
- **Don't soft-delete people who leave.** Flip `Status` to `archived` so past Run Log references stay valid.
- **Approval Tier is the lever.** Most teammates should sit at `light-review`. `always-review` slows agents to a crawl; reserve for finance/legal-adjacent people.
