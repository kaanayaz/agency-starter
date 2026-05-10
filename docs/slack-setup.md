# Setting up your Slack app

This is the doc that turns your Slack workspace into the operating channel for your AI agents. Allow ~30 minutes the first time. You only do this once.

> **Why bother?** Your agents will post messages, ask for approvals, and reply in threads using their own personas (custom name + avatar per agent). Without a Slack app, every message would come from a generic Claude account and the audit trail would be a mess. With your own app, the agents *are* part of your team.

---

## Step 1 — Create the app

1. Go to https://api.slack.com/apps
2. Click **Create New App** → **From scratch**
3. App Name: `Agency Bot` (or whatever your agency name is — this is the umbrella; individual agent personas are set per-message)
4. Pick your workspace
5. Click **Create App**

---

## Step 2 — Add bot scopes

In the left sidebar, click **OAuth & Permissions**. Scroll to **Bot Token Scopes**. Click **Add an OAuth Scope** and add **all** of these:

| Scope | Why we need it |
|---|---|
| `chat:write` | Post messages |
| `chat:write.customize` | Post with custom username + avatar (each agent gets its own persona) |
| `channels:history` | Read channel messages (so the Orchestrator can detect feedback in threads) |
| `channels:read` | List channels |
| `groups:history` | Read private-channel messages |
| `groups:read` | List private channels |
| `users:read` | Look up Slack user IDs (so agents can `<@mention>` the right person) |
| `files:write` | Upload generated decks/PDFs into Slack |
| `reactions:write` | Acknowledge feedback with an emoji |

> **Heads up:** `channels:history` + `groups:history` lets your bot see messages in any channel it's invited to. That's what enables the feedback loop where your replies in a thread teach the agent. Don't add the bot to channels with confidential client data unless you're OK with that.

---

## Step 3 — Install to your workspace

Still on **OAuth & Permissions**, scroll up. Click **Install to Workspace**. Approve.

You'll be redirected to a page showing a **Bot User OAuth Token** that starts with `xoxb-`. **Copy this.** This is the token Claude will use.

---

## Step 4 — Create the agency channel

In Slack:

1. Create a channel named `#ops` (or `#claude` or `#agents` — pick one).
2. Invite your bot: in the channel, type `/invite @Agency Bot` (or whatever you named it in step 1).
3. Pin a short description: *"Operations channel for the Claude agents. Drafts land here for review. Reply in-thread to give feedback."*
4. Get the channel ID: right-click the channel name → **View channel details** → scroll to the bottom → copy the ID (starts with `C`).

---

## Step 5 — Give Claude the credentials

In Terminal:

```bash
claude --set-env SLACK_BOT_TOKEN=xoxb-...                    # paste your token
claude --set-env SLACK_CHANNEL=C0XXXXXXXX                    # paste your channel ID
```

(Or, in your shell profile, `export SLACK_BOT_TOKEN=...` and `export SLACK_CHANNEL=...` — same effect.)

Verify:

```bash
echo $SLACK_BOT_TOKEN | cut -c1-5    # should print "xoxb-"
echo $SLACK_CHANNEL                   # should print your channel ID
```

---

## Step 6 — Smoke test

In a Claude Code session:

```
Send a test message to the ops channel from a "Test Agent" persona.
```

You should see a message in your `#ops` channel posted by `Test Agent` with a randomly generated avatar. If yes, you're done.

If you see `not_in_channel` — the bot isn't invited; do step 4.2 again.
If you see `invalid_auth` — the token is wrong; redo step 3.

---

## Step 7 — Add per-agent personas

We don't create a separate Slack app per agent. Instead, every agent in this system passes a custom `username` and `icon_url` when it posts, so the same bot speaks as different personas. Avatars are auto-generated from https://api.dicebear.com so you don't need to host images.

Defaults set in the plugin:

| Agent | Slack username | Icon |
|---|---|---|
| Orchestrator | `Orchestrator` | adventurer / `agency-orchestrator` |
| Invoice Reviewer | `Ledger` | adventurer / `agency-ledger` |
| Outreach | `Pitch` | adventurer / `agency-pitch` |
| Deck Builder | `Easel` | adventurer / `agency-easel` |
| Finance | `Tally` | adventurer / `agency-tally` |

You can rename or re-skin any of these per agency. Edit `plugin/agents/<name>.md` and change the `username` / `icon_url` fields.

---

## Step 8 — Decide your channel discipline

We strongly recommend:

- **One main channel** (`#ops`) where all agent posts land.
- **Replies happen in-thread**, not in the main channel. Thread replies are how you give feedback that the agent learns from.
- **No DMs from agents.** If an agent needs to reach a specific person, it `<@mentions>` them in `#ops`. This keeps everyone in the loop and prevents lost messages.

This mirrors how the buzzfy/sevde-egitim setup works in production.

---

## When something goes wrong

| Error | Likely cause | Fix |
|---|---|---|
| `not_in_channel` | Bot not invited to the channel | `/invite @YourBot` in the channel |
| `invalid_auth` | Wrong token or token revoked | Reinstall the app, copy the new token |
| `missing_scope` | A scope wasn't added in step 2 | Add the missing scope, reinstall, copy new token |
| `channel_not_found` | `SLACK_CHANNEL` wrong | Right-click channel → View details → copy ID |
| Agent message has no avatar | `chat:write.customize` scope missing | Add scope, reinstall |

If any of these stick, ping us — most resolve in <2 minutes.
