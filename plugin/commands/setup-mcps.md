---
name: setup-mcps
description: Connect Notion, Slack, Gmail, and Google Drive MCPs to Claude Code. Walks through each one and validates after.
---

You are wiring the four required MCPs into the operator's Claude Code. Slash commands and agents in this plugin assume all four are present; this is the gate that makes the rest work.

The operator is running Claude Code **desktop app** (not terminal). You cannot use `claude mcp add` from Bash. You either edit `~/.claude/settings.json` directly via the Edit tool, or you walk them through the desktop UI (Settings → MCP Servers → Add). Default to editing settings.json — it's faster and they don't have to leave the chat.

# Step 0 — Preflight

1. Confirm Claude in Chrome extension is installed (`mcp__Claude_in_Chrome__list_connected_browsers`). If not, stop and instruct them to install it first — several upcoming steps need it. Link: https://claude.ai/download.
2. Read `~/.claude/settings.json`. If it doesn't exist, create it with `{}`.
3. Print a one-line plan: *"I'll set up four MCPs in this order: Notion → Slack → Gmail → Drive. Each takes ~2 minutes. Ready?"*

Wait for go.

# Step 1 — Notion MCP

Notion needs an integration token before the MCP can connect.

1. **Check if already configured.** Try `mcp__notion-search`. If it works, skip to Step 2.
2. **Walk through integration creation:**
   - Use Chrome MCP to navigate to `https://www.notion.so/profile/integrations`.
   - Tell the operator: *"Click `+ New integration`. Name it `Agency Bot`. Type: Internal. Capabilities: Read content, Update content, Insert content. Save."*
   - Wait for them to confirm.
   - *"Copy the Internal Integration Secret (starts with `ntn_`) and paste it here."*
3. **Validate the token.** Make a direct API call to `https://api.notion.com/v1/users/me` with the token to confirm it works. If it fails, ask them to recheck the copy.
4. **Add to settings.json** under `mcpServers.notion`:
   ```json
   {
     "command": "npx",
     "args": ["-y", "@notionhq/notion-mcp-server"],
     "env": { "NOTION_TOKEN": "<their-token>" }
   }
   ```
   (If their plugin install already includes a different Notion MCP package, mirror that instead — don't overwrite an existing working config.)
5. **Tell them to restart Claude Code** so the new MCP loads. Pause and wait for confirmation.
6. **Re-validate.** After restart, call `mcp__notion-search` and confirm a real result. Mark Notion ✓.

# Step 2 — Slack MCP

Slack needs a bot token and a channel ID. If `/setup-slack` hasn't run yet, run it now (it produces both) — then return here.

1. Check `~/.claude/settings.json` for `SLACK_BOT_TOKEN` and `SLACK_CHANNEL`. If missing, invoke `/setup-slack` via SlashCommand and wait for it to complete.
2. **Add to settings.json** under `mcpServers.slack` with the token in env. Same restart-and-revalidate pattern as Notion.
3. **Smoke test:** post a one-line test message *"setup-mcps test, ignore"* to the configured channel. Confirm it lands. Mark Slack ✓.

# Step 3 — Gmail MCP

Gmail uses OAuth, not a static token. The MCP package handles the OAuth dance on first call.

1. Add the Gmail MCP entry to settings.json. Restart.
2. On first call, the MCP will trigger a browser OAuth flow. Tell the operator: *"A browser tab will open. Sign in with the agency's Gmail account and grant the requested scopes."*
3. Validate by listing the operator's labels via the MCP. Mark Gmail ✓.

# Step 4 — Google Drive MCP

Same OAuth pattern as Gmail. If they signed in with the same Google account for Gmail, Drive may be granted automatically.

1. Add the Drive MCP entry. Restart.
2. Validate by listing files in their Drive root. Mark Drive ✓.

# Step 5 — Final report

Print a clean checklist:

```
MCPs
─────
[x] Notion
[x] Slack
[x] Gmail
[x] Drive
```

Then suggest the next step: *"Run `/setup-notion` to build your Agency Ops workspace."* If `/setup-slack` was triggered earlier and didn't fully complete, point back to it instead.

# Edge cases

- **Restart loops.** If the operator restarts Claude Code mid-session, the slash command is interrupted. They'll need to re-run `/setup-mcps` — it's idempotent, the validate-first checks at each step skip what's already done.
- **OAuth stuck on a tab.** If the OAuth window doesn't open, the operator may have a popup blocker. Tell them to copy the OAuth URL from the MCP's stderr output and paste it manually. If they don't know how to find that, escalate via `/setup-help`.
- **Settings.json permissions.** On macOS, if Edit fails on `~/.claude/settings.json`, ask the operator to check whether the file is owned by another user (rare but happens after migrations). If they can't fix it themselves, escalate via `/setup-help`.

# Anti-confusion rules

- **One MCP at a time.** Don't paste a 4-MCP block into settings.json then restart once. The operator can't debug a multi-failure scenario; do them serially.
- **Always restart between adds.** New MCP entries don't take effect mid-session.
- **Never store the Notion or Slack tokens in plaintext anywhere outside settings.json.** No log files, no Slack messages, no echoed output.
