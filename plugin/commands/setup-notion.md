---
name: setup-notion
description: Build the seven Agency Ops databases in Notion from the plugin's source-of-truth templates.
---

You are constructing the operator's Notion workspace. The structure is defined in `notion-templates/01-team.md` through `07-schedule.md` (one file per DB or page). You read those files, then call Notion MCP tools to create the corresponding pages and databases in the operator's workspace.

This command is **idempotent**: if a piece already exists, skip it and move on. Never duplicate a page.

# Step 0 — Preflight

1. **Notion MCP must be connected.** Try `mcp__notion-search`. If it errors, stop and tell the operator to run `/setup-mcps` first.
2. **Tell the operator what's about to happen.** *"I'll create a top-level page called `Agency Ops` in your Notion workspace, then build seven databases under it. ~3 minutes. Ready?"*
3. Wait for go.

# Step 1 — Create the parent page

1. Search for an existing page literally named `Agency Ops` (or `🤖 Agency Ops`). If found, ask: *"Found an existing `Agency Ops` page. Use that as the parent, or create a fresh one?"*
2. If creating fresh: use Notion MCP `notion-create-pages` with title `Agency Ops`, parent = the user's workspace root (use the workspace's home / first available top-level location accessible to the integration).
3. The integration owns this page automatically — no separate "Connect to" step needed because the integration created it.
4. Save the new page's ID for the next steps.

# Step 2 — Build each of the seven DBs

For each template file in `notion-templates/`, in order:

| File | What to create |
|---|---|
| `01-team.md` | Database "Team" |
| `02-brand-voice.md` | Plain page "Brand Voice" with section headings |
| `03-entities.md` | Database "Entities" |
| `04-agent-todos.md` | Database "Agent Todos" |
| `05-learnings.md` | Database "Learnings" |
| `06-run-log.md` | Database "Run Log" |
| `07-schedule.md` | Database "Schedule" |

For each:

1. **Read the template file.** Parse the `## Schema` table — each row maps to a Notion property. Property types in the template (Title, Select, Multi-select, Number, Date, Checkbox, Text, Email, URL, Relation, Created time) map to Notion property types directly.
2. **For Select / Multi-select**, create the options listed in the `Options` column verbatim.
3. **For Relation properties**, create the DB *without* the relation first, then come back in a second pass (Step 3) and add the relation pointing at the now-existing target DB. Order matters: `Team` should be created before `Entities`, `Agent Todos`, `Schedule` (which all relate to Team).
4. **Create the DB** under the parent page via Notion MCP.
5. **Seed rows.** Parse the `## Seed rows` table and create one row per entry. Use placeholder names like `(Founder)`, `(Account Manager)` where the template uses them — the operator will edit these in `/setup-discovery`.
6. **For `Run Log`**, do NOT seed. The note in the template says "empty is the correct starting state" — respect it.
7. **For `Brand Voice`**, this is a *page*, not a DB. Create as a page and add Heading 2 blocks for each `### ` section in the template, with placeholder paragraph blocks beneath each heading saying *"To be filled during /setup-discovery."*

# Step 3 — Wire relations

Pass through the DBs a second time. For any property the template marked as `Relation → <DB>`:

1. Look up the target DB ID from your saved list.
2. Use Notion MCP to add the relation property to the source DB pointing at the target.

Targets in the templates:
- `Agent Todos.Owner Human` → Team
- `Agent Todos.Source Run Log` → Run Log
- `Schedule.Owner` → Team
- `Entities.Owner` → Team

# Step 4 — Verify

Query each DB by name and confirm:
- It exists
- The property count matches the template (within ±1 for any properties Notion auto-adds)
- Seeded rows are present (skip Run Log)

If any verification fails, print the failing DB and the mismatch. Don't try to auto-repair — the operator should re-run `/setup-notion` after looking at the diff (it's idempotent).

# Step 5 — Report

Print a clean summary:

```
Notion workspace built
──────────────────────
[x] Agency Ops (parent page)
[x] Team (3 seed rows)
[x] Brand Voice (page, sections empty — will fill in /setup-discovery)
[x] Entities (8 seed rows)
[x] Agent Todos (2 seed rows)
[x] Learnings (3 seed rows)
[x] Run Log (empty by design)
[x] Schedule (4 paused seed rows)
```

Then: *"Open Notion — `Agency Ops` is in your sidebar. Have a quick look. When you're back, run `/setup-discovery` to fill in your team and brand voice."*

# Anti-overreach rules

- **Don't seed real data.** The seed rows in the templates are placeholders. The operator's actual team, brand voice, and entities go in via `/setup-discovery`. Don't try to be clever and ask them now.
- **Don't auto-archive Run Log on creation.** That's a Notion DB setting and the templates note the operator should configure it. Don't try to do it via API; not all auto-archive settings are exposed.
- **Don't overwrite an existing Agency Ops page.** Always ask first.
- **Idempotency over completeness.** If a DB exists with the same name but a different schema, do NOT silently update it. Print the diff and ask the operator what to do.
