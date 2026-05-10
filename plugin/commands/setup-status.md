---
name: setup-status
description: Show what's been set up so far. Doesn't suggest a next step — use /start for that.
---

You are printing the current setup state. Same checks as `/start`, but you don't suggest what to do next and you don't drive any commands. Pure status read.

# Step 1 — Run the same detection as /start

Silently check:

1. Claude in Chrome extension installed
2. Notion MCP connected
3. Slack MCP connected
4. Gmail MCP connected
5. Drive MCP connected
6. `SLACK_BOT_TOKEN` + `SLACK_CHANNEL` in settings
7. `Agency Ops` parent page in Notion
8. The 7 DBs exist
9. Team DB has rows (count)
10. Brand Voice has real content
11. Recent green smoke test (within 7 days)

# Step 2 — Print one detailed table

Unlike `/start`, show counts and last-modified dates where useful:

```
Setup Status
─────────────
Plugin                : installed (v0.2.0)
Chrome extension      : connected
MCPs                  : Notion ✓ · Slack ✓ · Gmail ✓ · Drive ✓
Slack credentials     : present
Notion: Agency Ops    : created (last edited 2026-05-08)
Notion: 7 DBs         : 7/7 present
Notion: Team          : 4 rows
Notion: Brand Voice   : 8/8 sections filled
Notion: Entities      : 12 rows (8 Tool, 2 Service Tier, 2 Client Field)
Notion: Schedule      : 4 rows (0 active, 4 paused)
Smoke test            : green, 2 days ago
```

# Step 3 — That's it

Don't suggest a next step. Don't ask questions. End cleanly.

If the operator wants the next step, they run `/start`.

# Anti-confusion rules

- **No prompts.** This command is for the operator's own reference; it does not prompt for anything.
- **Stale data is fine.** This command only reflects what was true at run time. If the operator just edited Notion in another tab, that's not visible here unless they re-run.
- **Show empties as empties, not as failures.** A Schedule with 0 active rows isn't broken; it's the correct early-onboarding state. Don't redden the row.
