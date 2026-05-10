# Run Log

The audit trail of every Orchestrator run. You don't write here — read it when something seems off.

## Schema

| Property | Type | Options | Required | Notes |
|---|---|---|---|---|
| Timestamp | Date (with time) | — | yes | ISO; written by the Orchestrator at session start |
| Hour Local | Text | — | yes | `HH ${TZ}` format (e.g. `15 Europe/Istanbul`) |
| Ran | Multi-select | (auto-populated as agents are added) | yes | Agents dispatched this run, or `check-only` when nothing was scheduled |
| Local Pings | Multi-select | (auto-populated as agents are added) | no | Agents whose pending todos were pinged this run |
| Status | Select | ok, partial, override, check-only, failed | yes | High-level outcome |
| Override Path | Select | none, manual, feedback-driven | yes | `manual` = `$FORCE_AGENT_MODES`; `feedback-driven` = Step 3b.5 immediate dispatch |
| Notes | Text | — | no | One-line summary; longer notes if `partial` or `failed` |
| Session Duration (s) | Number | — | no | How long the Orchestrator session ran end-to-end |
| Slack Heartbeat URL | URL | — | no | Deep link to the Slack post for this run, if one was sent |

## Seed rows

Don't seed this DB. The Orchestrator's first run will populate it. Empty is the correct starting state.

## Read/write contract

- **Reads:** the Orchestrator (last 24h, to dedupe pings); humans during incident review
- **Writes:** the Orchestrator only — one row per run
- **Change rate:** one row per scheduled hour. With six run hours per day → ~180 rows/month
- **Retention:** prune entries older than 30 days. Notion can auto-archive on a date condition; configure it once

## How to use this DB during an incident

1. Sort by Timestamp desc, scope to the affected window.
2. Check Status — clusters of `failed` mean upstream brokenness (auth, MCP, rate limit). Clusters of `partial` mean a single agent is degrading.
3. Open the Slack Heartbeat URL on the suspect row to see what the team saw at the time.
4. Check Override Path — `manual` runs were operator-triggered (someone set `$FORCE_AGENT_MODES`); rule out before blaming the schedule.
5. If the issue traces to one agent, pull last 30 days of that agent's Learnings — recent corrections may be conflicting.

## Setup pitfalls

- **Don't edit Run Log rows.** They're an audit trail. If the data is wrong, fix the underlying agent or Orchestrator behavior, then let the next run produce a correct row.
- **Watch for `failed` clusters.** Three `failed` rows in 24h = something upstream is broken (auth expired, Notion permissions revoked, MCP down). Page on-call.
- **`partial` is normal.** It means at least one agent had a recoverable issue and the run completed others. Investigate the Notes field, not the Status alone.
- **`check-only` is also normal.** Hours where nothing was scheduled and no pings were due. No Slack heartbeat is sent for these by design — heartbeat-on-empty trains the team to ignore them.
- **Auto-archive the 30-day cutoff.** Notion DB setting → "auto-archive after date older than 30 days". Without this, querying last-24h gets slower over time as the table grows.
