# Agent Todos

The shared work queue between agents and humans. The most-read database in the system.

## What lives here

Anything that needs a human or another agent to act later, that isn't already a Slack draft awaiting a click. Three common shapes:

1. **Pending local work** — an agent flagged a task that requires a browser-bound tool the operator has to handle (e.g. "Approve invoice INV-0142 in [tool]")
2. **Cross-agent handoff** — one agent finished its part, the next can't run until a human triggers it
3. **Human-asked-for-it** — a person typed a request in Slack and the Orchestrator persisted it as a todo

## Schema

| Property | Type | Options | Required | Notes |
|---|---|---|---|---|
| Title | Title | — | yes | Imperative phrasing — "Approve INV-0142", "Review draft deck for Acme" |
| Owner Agent | Select | orchestrator (built-in), plus your own as you create them | yes | Populated as you create agents via `/codify-agent`. The agent that created the todo or that will eventually clear it |
| Owner Human | Relation → Team | — | conditional | Required for `pending` todos. The Orchestrator pings this person |
| Status | Select | pending, in-progress, done, blocked, cancelled | yes | Default `pending` |
| Tier | Select | routine, acceptable, critical | yes | Drives ping aggressiveness — `critical` pages outside working hours, the others wait for working hours |
| Due | Date | — | no | Soft deadline; the Orchestrator escalates Tier one notch 24h before due |
| Notes | Text | — | no | Free-form, including links to source artifacts |
| Created By | Select | agent, human | yes | Audit only |
| Created At | Created time | — | auto | Notion auto-populates |
| Source Run Log | Relation → Run Log | — | no | If this todo was emitted by an Orchestrator run, link it |
| Source Slack | URL | — | no | If from a Slack thread, paste the deep-link |

## Seed rows

Two examples to seed the DB shape — delete during discovery:

| Title | Owner Agent | Owner Human | Status | Tier | Notes |
|---|---|---|---|---|---|
| Approve invoice INV-0142 (your-invoice-tool) | (your-first-agent) | (Founder) | pending | acceptable | Vendor: Acme Corp. Amount: 4,200 TRY. Risk flags: none. Posted to #ops at <ts>. |
| Re-source 3 creators for Brand X campaign | (your-first-agent) | (Account Manager) | pending | routine | Original list was 12; client rejected 3 for tier mismatch. Re-source from same niche. |

## Lifecycle

- New todo → `pending`, owner pinged in `#ops` per Team rules
- Owner starts work → manually flips to `in-progress`
- Owner finishes → flips to `done`. Stays 7 days then auto-archives (Notion DB setting)
- Stuck? Flip to `blocked` and add a comment. The Orchestrator escalates blocked items in the next-day digest

## Read/write contract

- **Reads:** Orchestrator on every run (to decide who to ping); each agent on its own run (for its open todos)
- **Writes:** any agent (creates and updates its own todos); humans manually clear or comment
- **Change rate:** every Orchestrator run touches this; high-volume database

## Setup pitfalls

- **Owner Human is required for `pending`.** The Orchestrator skips todos with no owner, and they pile up invisibly. Add a Notion validation if possible (formula: `if(Status = pending && empty(Owner Human), "missing owner", "ok")`).
- **Don't over-tier.** `critical` should be rare — data risk, money risk, or client-down. If everything is `critical`, the page-after-hours rule will burn out your team in a week.
- **Don't reuse a todo across runs.** One todo = one piece of work. Closing one and opening a new one is correct; toggling `done` → `pending` confuses the Run Log audit trail.
- **Auto-archive setting**: in Notion DB settings → enable "auto-archive after 7 days for `done` items". Without this, the DB grows unboundedly and the Orchestrator's reads slow down.
- **Same-day re-pings are suppressed.** The Orchestrator pings each pending todo at most once per day in the agency's primary timezone. If a todo is genuinely critical and missed, manually @-mention the owner in #ops.
