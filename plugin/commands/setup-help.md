---
name: setup-help
description: Escalate a setup problem via email to the agency-starter maintainer. Captures recent context, sanitizes it, and sends from the operator's own Gmail.
---

You are escalating a stuck setup. The operator hit a wall during one of the `/setup-*` commands and needs a human (us, the plugin maintainers) to look. Your job is to capture enough context that the human responder doesn't need to ask follow-ups, and email it cleanly.

The support email is configured in `~/.claude/settings.json` under `agency_starter.support_email`. Default: `bugrakaanayaz@gmail.com`. The email is sent **from the operator's own Gmail account** via the connected Gmail MCP — the operator gets a copy in their Sent folder and can reply in-thread when the maintainer responds.

If Gmail MCP isn't connected or sending fails, fall back to opening a GitHub issue on the plugin's repo with the same body.

# Step 0 — Confirm intent

Ask: *"You want me to email the agency-starter maintainer about this? I'll capture the last command you ran, the error, and your setup-status snapshot. Nothing sensitive — no tokens. The email goes from your Gmail to <support_email>. (yes/no)"*

If no, exit.

# Step 1 — Gather context

1. **Last setup command run.** Read recent shell/session history if available; otherwise ask: *"Which `/setup-*` command was running when you got stuck?"*
2. **The error.** Ask: *"Paste the exact error you saw. If there was no error but it just hung or behaved wrong, describe what you expected vs what happened."*
3. **Setup status snapshot.** Run the same detection as `/setup-status` (programmatically, not by invoking the command — you want the data, not a printed table).
4. **Plugin version.** Read from plugin metadata.
5. **Claude Code version.** Capture if available.
6. **OS.** macOS / Windows. (Plugin is Mac-first but Windows operators exist.)

# Step 2 — Sanitize

Strip from all collected data:

- Slack bot tokens (start with `xoxb-`, `xoxp-`, `xapp-`)
- Notion integration tokens (start with `ntn_`, `secret_`)
- Email addresses other than the operator's own (which the maintainer already has via the plugin install)
- Any text the operator marked as private during the conversation

If you find a token in their pasted error, redact it and note: *"(redacted: looked like a token)"*

# Step 3 — Build the email

**Subject:** `[agency-starter] Setup help: <operator-name> stuck on /<command>`

**Body** (plaintext, no HTML):

```
Setup help requested

Operator: <name> <<email from plugin install>>
Plugin: v<plugin_version>
Claude Code: v<cc_version>
OS: <os>

Stuck on: /<command>
Error: <one-line summary>

Detail:
<sanitized error text or behavior description>

Setup status:
  MCPs: Notion ✓ · Slack ✗ (auth) · Gmail ✓ · Drive ✓
  Notion DBs: 7/7
  Team rows: 4
  Brand Voice: filled
  Smoke test: red (last run 2 days ago — Slack auth failed)

What they tried:
- <their description, if any>

---
Sent by /setup-help from agency-starter v<plugin_version>.
Reply to this email — the operator is on this thread.
```

# Step 4 — Send

1. Send via Gmail MCP (`mcp__GMAIL_SEND_EMAIL` or equivalent) from the operator's connected Gmail account:
   - **To:** `<support_email>` (default `bugrakaanayaz@gmail.com`)
   - **From:** the operator's Gmail (set automatically by the MCP — uses whatever account is connected)
   - **Subject:** as in Step 3
   - **Body:** as in Step 3
2. Capture the resulting Gmail message ID / thread ID.
3. Tell the operator: *"Sent from your Gmail to `<support_email>`. Check your Sent folder for the thread. Reply lands in your inbox when the maintainer responds — typically within a working day. (No formal SLA yet — we're early.)"*

If sending fails (Gmail MCP not connected, auth expired, network), fall back to:

1. Open a GitHub issue on the plugin's repo with the same body in the issue description
2. Tell the operator: *"Couldn't send via Gmail (<reason>). Created a GitHub issue at <url> instead. Watch that thread for replies — you'll need to be signed into GitHub to comment."*

# Step 5 — Log

Append to `~/.claude/agency-starter/help-requests.jsonl`:

```json
{"ts": "<ISO>", "command": "<stuck-on>", "method": "email|github", "thread_id": "<gmail thread id or issue url>", "resolved": false}
```

The operator can mark resolved manually later, or another command can flip the flag once the issue is closed.

# Anti-confusion rules

- **Confirm before sending.** Setup help emails go off the operator's own Gmail account — they should always opt in. The from-address is theirs.
- **No tokens, ever.** Even if the operator pastes a token in error, redact and warn them in-chat: *"I noticed a token in your paste — I redacted it before sending. Rotate it via your tool's UI to be safe."*
- **One escalation at a time.** If `help-requests.jsonl` has an unresolved entry from the same operator in the last hour, ask before sending a second email — the maintainer is probably already looking at the first one.
- **Don't promise an SLA you don't have.** Until a formal SLA is set, say *"typically within a working day"* and leave it at that.
- **Don't BCC anyone.** The reply chain stays clean if the email is just operator → maintainer with no hidden recipients.
