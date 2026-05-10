---
name: suggest-mcp
description: Map a user intent like "I want to check our HubSpot deals" to a known MCP server, and either install it or escalate. Called by the pattern-recognizer skill when it spots a missing-tool reach.
---

You are translating "I want to do X with [tool]" into either (a) an MCP install + connection flow, or (b) a clean "no available MCP" response.

You're typically called by the `pattern-recognizer` skill after it detected the operator wanted to use a tool Claude can't reach. Your job: map intent → MCP → install. The operator does not know what an MCP is; you describe it as "connecting Claude to <tool>".

# Step 1 — Identify the tool

The caller passes you the operator's intent, often verbatim. Extract the tool name. Examples:

| Operator said | Tool |
|---|---|
| "Can you check our HubSpot pipeline?" | HubSpot |
| "Pull the latest issue from our Linear" | Linear |
| "What's in our Stripe dashboard for last week?" | Stripe |
| "Look at the Figma file for client X" | Figma |
| "Read the latest Asana tasks" | Asana |
| "Check our QuickBooks for this month" | QuickBooks |

If the tool name is ambiguous ("our project tool"), ask once: *"Which tool specifically?"*

# Step 2 — Look up against the known MCP registry

Check, in order:

1. **MCPs already installed** — list current MCPs in `~/.claude/settings.json`. If the tool is already there, the issue is auth, not install. Route to re-auth flow.
2. **MCPs in the operator's connected `mcp-registry`** — call `mcp__mcp-registry__search_mcp_registry` with the tool name. If a match exists, capture install instructions.
3. **Known commercial MCPs** maintained by the tool's vendor or by Anthropic. Common ones include:
   - HubSpot (community + official versions exist)
   - Linear (official)
   - Stripe (official, configured via Stripe plugin in this codebase)
   - Figma (official, configured via Figma plugin)
   - Notion, Slack, Gmail, Drive (already required by this plugin)
4. **No known MCP** — fall through to Step 4.

# Step 3 — On match

Tell the operator in plain language:

> Yes, there's a way to connect Claude to <tool>. Want me to set it up? It takes ~3 min and unlocks me reading/writing in <tool> for any future session.

If yes:

1. **Add the MCP entry to `~/.claude/settings.json`** under `mcpServers.<tool-key>` using the install spec from the registry or known config.
2. **Walk through any auth step** — most third-party MCPs use OAuth (browser flow on first call) or a static API key (paste it like the Notion token flow in `/setup-mcps`).
3. **Tell the operator to restart Claude Code** so the new MCP loads.
4. **After restart, validate** — call a small read on the new MCP. Confirm it returns data.
5. **Report:** *"Connected. <Tool> is now available in any future session — just ask."*

# Step 4 — On no match

Tell the operator:

> I don't know of a way to connect Claude to <tool> directly. A few options:
>
> 1. **Use the tool's API manually** — if <tool> has an API and you have a key, I can call it via web requests, but it's slower and breaks more often than a real MCP.
> 2. **Ask us to build one** — if this is a tool you'll keep wanting to reach, drop a note in `/setup-help` and we'll add it to the plugin.
> 3. **Workaround** — for one-offs, tell me what's in <tool> and I'll work from your description.
>
> Which?

Capture their answer and act on it. Don't promise build timelines.

# Step 5 — Logging

Append to `~/.claude/agency-starter/mcp-suggestions.jsonl`:

```json
{
  "ts": "<ISO>",
  "tool": "<name>",
  "outcome": "installed | declined | no-match | rerouted-to-help",
  "operator_intent": "<original quote>"
}
```

The Orchestrator reads this monthly to spot repeat "no-match" entries — those become candidates for the plugin maintainers to build an MCP for.

# Anti-overreach rules

- **Don't install MCPs the operator didn't ask about.** If they said "check HubSpot," don't volunteer Linear because it might also help them.
- **Don't install MCPs from untrusted sources.** Only the registry, vendor-official, or Anthropic-published. If you find a community MCP that looks useful but unverified, mention it but don't install: *"There's a community-built one at <URL>. We haven't reviewed it. Want me to flag for the plugin team to evaluate?"*
- **Static API keys are tokens — same handling as Notion / Slack tokens.** Never log, never echo back, store only in settings.json.
- **OAuth flows can stall.** If the OAuth window doesn't open or the operator can't complete it (popup blocker, wrong account), gracefully back out and route to `/setup-help`. Don't loop on retry.
