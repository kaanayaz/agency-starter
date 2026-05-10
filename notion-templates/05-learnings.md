# Learnings

Where institutional knowledge that didn't fit in Brand Voice or Entities accumulates over time. One database, two recommended views.

## Two recommended views

In Notion, create two **views** on the same DB:

1. **Per-agent learnings** — group by `Agent`, sort by date desc. The view each agent reads at run start.
2. **Cross-agent signals** — filter `Type = cross-agent`, all dates. The view the Orchestrator scans when assembling context for runs that touch multiple agents.

## Schema

| Property | Type | Options | Required | Notes |
|---|---|---|---|---|
| Date | Date | — | yes | When the observation was made (not when promoted) |
| Agent | Select | orchestrator (built-in), all (cross-agent), plus your own as you create them | yes | Which agent this teaches. Populated as you create agents via `/codify-agent` |
| Type | Select | per-agent, cross-agent | yes | Filter for the views above |
| Observation | Text | — | yes | The actual thing learned, in plain language |
| Source | Text | — | yes | Where it came from. Stable IDs: `slack:{parent_ts}/{reply_ts}`, `manual:{operator-name}`, `runlog:{id}` |
| Classification | Select | directive, correction, question, feature-request, pattern | yes | What kind of learning this is |
| Promotion Status | Select | Log, Active Insight, Active Rule, Graduated to Brand Voice, Graduated to Entities, Retired | yes | Where this learning sits on its lifecycle |
| Times Seen | Number | — | yes | Incremented when the same observation recurs. 3+ triggers promotion review |
| Active Rule | Checkbox | — | no | If true, every run of `Agent` loads this in context. Use sparingly — too many active rules dilute attention |
| Notes | Text | — | no | Free-form context |

## Promotion ladder

```
Log              → captured but not loaded into agent context. Pruned after 30 days unless promoted.
Active Insight   → loaded for the named Agent on relevant runs (Orchestrator decides relevance heuristically).
Active Rule      → always loaded for the named Agent. The agent treats it as a hard constraint.
Graduated to Brand Voice    → moved to the Brand Voice page; row in Learnings is set to Retired with a back-link.
Graduated to Entities       → moved to the Entities DB; same retirement.
Retired          → kept for audit, not loaded.
```

The Orchestrator handles `Log → Active Insight` automatically when `Times Seen ≥ 3`. Promotion to `Active Rule` and graduation requires a human edit — too important for an agent to self-promote.

## Seed rows

| Date | Agent | Type | Observation | Source | Classification | Promotion Status | Times Seen | Active Rule |
|---|---|---|---|---|---|---|---|---|
| (today) | (your-first-agent) | per-agent | Vendor "Acme Co" sometimes invoices with no VAT line — they're VAT-exempt registered. Don't flag as risk. | manual:bugra | correction | Active Rule | 1 | yes |
| (today) | (your-second-agent) | per-agent | Don't open a cold email with "Hope you're well". Operator rejects every draft that does. | slack:1715000000.000000/1715000010.000000 | directive | Active Rule | 4 | yes |
| (today) | all | cross-agent | The client "Brand X" prefers all comms in Turkish despite being a multinational. Persists across outreach drafts and deck copy. | manual:bugra | pattern | Active Insight | 2 | no |

## Read/write contract

- **Reads:** every agent loads its own `Active Rule` rows + last-30-days `Active Insight` rows on each run; the Orchestrator reads cross-agent signals
- **Writes:** Orchestrator (Step 3b — feedback relay); any agent that wants to log a self-observation; humans editing classifications and promotion statuses
- **Change rate:** every Slack thread reply that's classified as feedback creates a row

## Setup pitfalls

- **Active Rule is expensive.** Every active rule lengthens every relevant agent's prompt. If you have more than ~10 active rules per agent, the agent starts forgetting some. Promote sparingly, retire aggressively.
- **Source format matters.** The Orchestrator dedupes on Source — if you re-write Source on a row, you'll get duplicate entries on the next pass.
- **Don't edit Observation text after creation.** Add a new row instead. Old observations might still be referenced from Run Log notes or other Learnings entries.
- **Times Seen is mostly manual.** The Orchestrator increments when it catches a near-duplicate, but human pattern-matching catches more. If you see the same correction recur, increment by hand and update Promotion Status when it crosses 3.
- **Retired ≠ deleted.** A retired row still surfaces in audit reads. Delete only if the row was a mistake (duplicate, wrong agent).
