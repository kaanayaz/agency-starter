---
name: start
description: Entry point for the agency-starter plugin. Detects what's set up and tells you what to run next.
---

You are running `/start`. The operator just installed the plugin or is mid-onboarding. Your job is to figure out where they are and point them to the right next slash command. Be brief. They don't know the system yet.

# Step 0 — Language preference

Before anything else, check the operator's preferred system language at `~/.claude/settings.json` → `agency_starter.system_language`.

- **If set:** use it for the rest of this session. All your output to the operator goes in that language.
- **If unset and this looks like a first run** (no agency-starter keys in settings.json yet): ask in English first, then in their detected browser language if different — *"What language should I use? (e.g. English, Türkçe, Español, Français.) You can change this anytime by typing 'switch language'."* Save their answer to `agency_starter.system_language` and continue in that language.
- **If unset but other agency-starter state exists** (mid-onboarding): default to English silently and continue. Don't interrupt to ask for language preference if they're already in flow.

Per-session override: if the operator types in a different language than the saved preference, mirror them this session and ask once at the end whether to update the preference.

Note: `system_language` is the language *you talk to the operator in*. The language agents *produce content in* (Slack drafts, deck copy, outreach) is set in Brand Voice → Primary Language and may be different. Don't conflate.

# Step 1 — Silent state check

Run all of these without printing intermediate output:

1. **Claude in Chrome extension** — try a no-op `mcp__Claude_in_Chrome__list_connected_browsers`. If the tool isn't found, the extension isn't installed.
2. **Notion MCP connected** — try `mcp__notion-search` with an empty query. Tool-not-found = not installed; auth error = installed-but-not-authed.
3. **Slack MCP connected** — try a small Slack MCP read.
4. **Gmail MCP connected** — try a small Gmail MCP read.
5. **Google Drive MCP connected** — try a small Drive MCP read.
6. **Slack credentials present** — read `~/.claude/settings.json` and check for `SLACK_BOT_TOKEN` and `SLACK_CHANNEL` (or env vars).
7. **"Agency Ops" parent page in Notion** — search for it via Notion MCP.
8. **The 7 DBs exist under it** — query each by name (Team, Brand Voice, Entities, Agent Todos, Learnings, Run Log, Schedule).
9. **Team DB has rows** — count.
10. **Brand Voice page has content** — fetch it, check it isn't empty.
11. **Recent smoke test** — read `~/.claude/agency-starter/smoke-test.log` for a green entry in the last 7 days.
12. **Stop hook wired** — read `~/.claude/settings.json` for `hooks.Stop` referencing the plugin's `post-session-noticer.py`. If the plugin manifest auto-wires, this is already true; if not, offer to add it after the main checklist.
13. **Pending noticer suggestions** — count entries in `~/.claude/agency-starter/noticer-queue.jsonl` newer than the last `/start` invocation.

# Step 2 — Print one compact status

Use plain checkmarks. No emoji elsewhere.

```
Setup status
─────────────
[ ] Claude in Chrome extension
[ ] MCPs (Notion, Slack, Gmail, Drive)
[ ] Slack app + #ops channel
[ ] Notion workspace built
[ ] Discovery (Team, Brand Voice, Entities)
[ ] Smoke test
[ ] Noticer hook wired
```

Replace `[ ]` with `[x]` for items that pass. Don't show diagnostic detail unless asked.

If pending noticer suggestions exist (Step 1, check 13), append a one-liner under the checklist:

```
Pending suggestions: <N> queued from recent sessions. Want to review them now? (yes/later)
```

If they say yes, walk through each queued suggestion — read it from the queue file, present the operator-facing message (per `pattern-recognizer` skill templates), capture yes/no, act on yes (call `/codify` for repeat-task, write Active Rule for standing-rule, etc.), append to `noticer-rejected.jsonl` for no, and remove from the queue either way.

# Step 3 — Suggest exactly one next step

The first unchecked item dictates the next command. Map:

| First missing item | Run next |
|---|---|
| Chrome extension | Print install link (https://claude.ai/download), then `/start` again |
| Any MCP | `/setup-mcps` |
| Slack credentials | `/setup-slack` |
| Notion workspace | `/setup-notion` |
| Discovery rows | `/setup-discovery` |
| Smoke test | `/setup-smoke-test` |
| Hook unwired | Add the Stop-hook snippet to `~/.claude/settings.json` (point to `${CLAUDE_PLUGIN_ROOT}/hooks/post-session-noticer.py`); confirm with operator before editing |
| All checked | `/first-task` (or `/import-cowork` if they came from Claude Cowork) |

End with two lines:

> Next: run `/<command>`.
> I can run it for you now if you want — just say yes.

# Step 4 — Drive if asked

If the operator says yes (or anything affirmative), invoke the suggested command via the SlashCommand tool. If they say no or want to wait, exit cleanly.

# Anti-confusion rules

- **Don't dump diagnostics.** A green checklist is one line: *"You're fully set up. Run `/first-task` to start codifying tasks."*
- **Don't auto-skip ahead.** If MCPs are connected but Notion DBs aren't built, don't dive into building DBs without confirmation — the operator might have run `/setup-mcps` for an unrelated reason.
- **Don't use jargon pre-discovery.** The words "Active Rule", "Schedule DB", "Orchestrator" mean nothing to a new operator. Save them for after `/setup-discovery` completes.
- **If something fails to detect for an unclear reason, ask once.** Better to clarify than to guess and route them down the wrong path.
