---
name: setup-smoke-test
description: End-to-end check that everything is wired. Reports green/red for each component and writes a log entry.
---

You are running a comprehensive verification pass. Every component the system depends on gets a single concrete test. The output is a one-screen report and a log entry at `~/.claude/agency-starter/smoke-test.log`.

# Step 0 — Preflight

Confirm: *"Running the full system smoke test. ~2 minutes. Nothing is sent externally — drafts and test messages only."*

# Step 1 — Run each test, capture pass/fail

| # | Test | What | Pass criteria |
|---|---|---|---|
| 1 | Plugin install | List installed plugins; confirm `agency-starter` is among them | Found |
| 2 | settings.json | Read `~/.claude/settings.json`; confirm required keys present (`SLACK_BOT_TOKEN`, `SLACK_CHANNEL`) | Both present |
| 3 | Notion MCP | Call `mcp__notion-search` with empty query | Returns ≥1 result |
| 4 | Slack MCP | Call a small Slack MCP read | Returns successfully |
| 5 | Gmail MCP | List inbox labels via Gmail MCP | Returns ≥1 label |
| 6 | Drive MCP | List 1 file from Drive root | Returns 1 file (or empty-but-no-error if account is empty) |
| 7 | Notion: Agency Ops page | Search for `Agency Ops` page | Found, ID returned |
| 8 | Notion: 7 DBs | Query each by name (Team, Brand Voice, Entities, Agent Todos, Learnings, Run Log, Schedule) | All 7 found |
| 9 | Notion: Team has rows | Count Team rows | ≥1 |
| 10 | Notion: Brand Voice filled | Fetch Brand Voice page; check Tone section is non-placeholder | Real content found |
| 11 | Slack: post test message | Post `"smoke test, ignore"` to `$SLACK_CHANNEL` | `ok: true` |
| 12 | Slack: read test message back | Read recent channel history; find the test message | Found |
| 13 | Slack: bot identity | Confirm the test message was posted as `Agency Bot` (or your renamed app) | Yes |
| 14 | Slack: custom-username post | Post a message as username `Test Persona` with a custom icon | Posts and renders with custom name/avatar |
| 15 | Orchestrator dry-run | Invoke orchestrator agent with `$FORCE_AGENT_MODES=orchestrator:check` | Completes without error, writes a Run Log row |
| 16 | Run Log row appears | Query Run Log for the just-written entry | Found, with `Status: check-only` |

For each, record `pass` or `fail` plus a one-line reason.

# Step 2 — Print the report

```
Smoke test (timestamp)
────────────────────────────
[x] Plugin installed
[x] settings.json has required keys
[x] Notion MCP
[x] Slack MCP
[x] Gmail MCP
[x] Drive MCP
[x] Notion: Agency Ops parent page
[x] Notion: all 7 DBs present
[x] Notion: Team has rows
[x] Notion: Brand Voice has real content
[x] Slack: post test message
[x] Slack: read message back
[x] Slack: bot identity correct
[x] Slack: custom-username posts work
[x] Orchestrator dry-run completes
[x] Run Log row appears
────────────────────────────
Result: GREEN — fully wired.
```

If any test fails, print the failures with the one-line reason and stop. Don't try to auto-repair.

# Step 3 — Write the log entry

Append to `~/.claude/agency-starter/smoke-test.log`:

```
{"ts": "<ISO>", "result": "green|red", "failures": [...], "duration_s": N}
```

The `/start` command reads this file to decide whether to surface the smoke-test step.

# Step 4 — Suggest the next step

- **All green:** *"Fully wired. Run `/first-task` to codify your first real task."*
- **Any red:** *"<N> tests failed. Most common fixes are in `/setup-help`. If you can't unblock, run `/setup-help` to escalate to support."*

# Anti-confusion rules

- **Don't run partial tests.** All 16 every time. The point is a single trustworthy snapshot.
- **Test messages must be obvious as test messages.** Use the literal string `smoke test, ignore` so humans skimming the channel know to dismiss it.
- **Clean up after yourself.** Delete the test Slack messages from the channel after capturing the read-back result. Same for any Notion test pages if you created them. The Run Log entry stays — it's the audit trail.
- **`failed` in this command is different from `failed` in Run Log.** A smoke test failure means a setup step is broken, not that an agent run failed.
