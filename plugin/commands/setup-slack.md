---
name: setup-slack
description: Walk through creating your Slack app and #ops channel. Validates the bot token before saving.
---

You are guiding the operator through Slack app creation. The web flow lives at `api.slack.com/apps` — Claude in Chrome MCP navigates and reads the page back, the operator clicks. You verify each step before moving on.

If Chrome MCP isn't available, fall back to text instructions from `docs/slack-setup.md` and ask the operator to paste tokens manually at the right moments.

# Step 0 — Preflight

1. Check `~/.claude/settings.json` for an existing `SLACK_BOT_TOKEN`. If present, ask: *"You already have a Slack token configured. Skip Slack setup, or redo it?"*
2. Confirm Chrome extension is connected. If not, the doc-based fallback applies for the rest of this command.
3. Ask: *"Do you already have a Slack workspace for the agency, or do we need to create one?"*
   - If new: walk them through workspace creation at `slack.com/get-started` first. Pause until they're signed into a workspace.
4. Print a one-line plan: *"I'll guide you through creating an app called `Agency Bot`, adding the right scopes, installing it, getting the bot token, and creating an `#ops` channel. ~10 minutes. Ready?"*

Wait for go.

# Step 1 — Create the app

1. Chrome MCP navigates to `https://api.slack.com/apps`.
2. Read the page. If the operator has existing apps, list them and confirm we're creating new.
3. *"Click `Create New App` → `From scratch`. Name: `Agency Bot`. Pick your workspace. Click Create App."*
4. Wait for them to confirm.
5. Read the page back to confirm the app exists.

# Step 2 — Add OAuth scopes

1. Navigate to the app's `OAuth & Permissions` page (left sidebar in Slack's app config).
2. Tell the operator: *"Scroll to `Bot Token Scopes`. I'll list nine scopes — click `Add an OAuth Scope` and add each."*
3. List them one per line:
   - `chat:write`
   - `chat:write.customize`
   - `channels:history`
   - `channels:read`
   - `groups:history`
   - `groups:read`
   - `users:read`
   - `files:write`
   - `reactions:write`
4. After they confirm, read the page and verify all nine are present. If any are missing, name them and ask the operator to add the gap.

# Step 3 — Install to workspace

1. *"Scroll up. Click `Install to Workspace`. Approve the prompt."*
2. After approval, the page shows a `Bot User OAuth Token` starting with `xoxb-`.
3. *"Copy that token and paste it here. Don't share it elsewhere — I'll store it in your settings only."*
4. Wait for the paste.

# Step 4 — Validate the token

Before saving, confirm the token works:

```bash
curl -s -X POST https://slack.com/api/auth.test \
  -H "Authorization: Bearer ${PASTED_TOKEN}"
```

Expect `"ok": true`. If `invalid_auth`, ask them to re-copy. If `missing_scope`, name the missing scope and route back to Step 2.

# Step 5 — Create the #ops channel

1. *"In Slack itself (not the api.slack.com tab), create a public channel called `#ops`. (Or pick an existing channel — just tell me which.)"*
2. *"In that channel, type `/invite @Agency Bot` to add the bot."*
3. *"Right-click the channel name → View channel details → scroll to the bottom → copy the channel ID (starts with `C`)."*
4. *"Paste the channel ID here."*
5. Validate by posting a one-line test message *"Agency Bot setup test, ignore"* via the token. Confirm it lands.

# Step 6 — Save credentials

Edit `~/.claude/settings.json` to add:

```json
"env": {
  "SLACK_BOT_TOKEN": "<token>",
  "SLACK_CHANNEL": "<channel ID>"
}
```

Don't print the token back. Confirm only that it's saved.

# Step 7 — Report

```
Slack
─────
[x] App created: Agency Bot
[x] 9 scopes added
[x] Token validated and saved
[x] #ops channel created with bot invited
[x] Test message posted
```

Then: *"Slack is wired. Run `/setup-mcps` to wire the Slack MCP, or run `/start` to see what's next overall."*

# Edge cases

- **`not_in_channel` on test post** — the bot wasn't invited. Re-do the `/invite` step.
- **`missing_scope` mid-flow** — Slack apps cache scopes; after adding new ones, they may need to re-install (Step 3) and re-copy the token. Walk them through it.
- **Two-factor on Slack workspace** — if creating a new workspace required 2FA setup, account creation can take several minutes. Don't push them to rush.

# Anti-confusion rules

- **One scope at a time.** Don't paste the full nine and say "add these all." Operators new to Slack apps get lost in the scope picker.
- **Verify the page after every step.** If they say "done" but Chrome MCP shows the page hasn't updated, the click probably didn't register — ask them to click again rather than moving on.
- **Token never appears in your output.** Not even truncated. The validation result (`"ok": true`) is enough.
