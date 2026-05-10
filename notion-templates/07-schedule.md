# Schedule

Controls when each agent runs. The Orchestrator reads this every hour and dispatches agents whose row matches the current hour, day, and `Status = active`.

## Schema

| Property | Type | Options | Required | Notes |
|---|---|---|---|---|
| Agent | Select | (empty by default; populated as you create agents via `/codify-agent`) | yes | One row per agent (or one row per agent-mode combination) |
| Mode | Select | prepare, execute | yes | `prepare` = drafts only, no external sends. `execute` = the agent may take external actions. Default `prepare` for everything until trust is earned |
| Run Hours | Multi-select | 00, 03, 06, 09, 12, 15, 18, 21 | yes | Hours in the agency's primary timezone (from Team DB row 1) |
| Days | Multi-select | Mon, Tue, Wed, Thu, Fri, Sat, Sun | yes | Which days this row is active |
| Status | Select | active, paused, draft | yes | Only `active` rows are dispatched. `paused` keeps the row but skips it. `draft` is for rows being designed but not yet ready |
| Owner | Relation → Team | — | yes | The human responsible for this scheduled agent. They get pinged if it fails repeatedly |
| Execution Order | Number | — | no | When multiple agents run the same hour, dispatch in this order. Default alphabetical by Agent name |
| Stability Required | Select | stable, tested, draft | yes | The Orchestrator only dispatches commands at this stability or higher. Default `stable` for all schedule rows |
| Last Run | Date | — | no | Updated by the Orchestrator after each dispatch |
| Notes | Text | — | no | Free-form, e.g. "Reduced from hourly to 3-hourly after creator-outreach was rate-limited" |

## Seed rows

**No seed rows.** Schedule fills as you create your own agents (via `/codify-agent`) and decide they're stable enough to schedule. Day-one Schedule should be empty.

When you do add a row, treat it as drafty until the underlying commands have hit `stable`. Status starts at `paused` or `draft` — you flip to `active` only when you trust the agent to run unattended.

Example shape (do **not** copy as-is — the agent name `(your-agent)` is a placeholder):

| Agent | Mode | Run Hours | Days | Status | Owner | Stability Required | Notes |
|---|---|---|---|---|---|---|---|
| (your-agent) | prepare | 09, 15 | Mon, Tue, Wed, Thu, Fri | paused | (Owner) | stable | Activate after 8 successful drafted runs |

## Picking Run Hours

- **Don't run agents every hour by default.** Most agency work is bursty, not continuous. Two to four hours per day is typical.
- **Avoid the top of the hour for non-critical agents.** If multiple rows fire at `09`, the Orchestrator dispatches them serially in one session — fine, but the first agent's output sometimes triggers feedback the second agent should see. Spreading by 15 min helps; Notion's multi-select can't express that, so treat the hour as the *start* and accept some serialization.
- **Run during working hours unless there's a reason not to.** A draft posted at 03:00 sits unattended until 09:00 anyway. The Orchestrator can read but humans can't react.

## Read/write contract

- **Reads:** the Orchestrator on every run
- **Writes:** humans only (you flip Status, you adjust Run Hours)
- **Change rate:** weekly during weeks 2-4 of onboarding; monthly thereafter

## Setup pitfalls

- **Status defaults to `draft`.** Agents you set up in advance for "later" should sit in `draft`, not `active`. The Orchestrator dispatches every `active` row even if you weren't expecting it to.
- **Mode `execute` is the dangerous flag.** Flipping it without an explicit team decision is the most common way an agent over-reaches. Treat it like a deploy: two-person review, log the change in Run Log notes.
- **Stability Required is a backstop.** Even if a Schedule row is `active`, the Orchestrator won't dispatch a command below the listed stability. Useful for staged rollout: schedule something for `stable` two weeks before the command is actually ready, and it sits idle until then.
- **Local agents fire as todos, not direct dispatch.** A `runtime: local` agent (like `invoice-reviewer`) cannot be cloud-dispatched. The Orchestrator instead creates a pending Agent Todo for the operator to run the agent manually. Schedule it normally with `Mode: prepare` — the routing difference is handled by the Orchestrator, not by you.
- **Don't over-schedule the Orchestrator itself.** It's already a recurring routine; it doesn't need a Schedule row. If you see one for `orchestrator`, delete it.
