# Welcome to agency-starter

A 3-step quickstart. Gets you from "Claude Code installed" to "Claude is running my first task" in about 90 minutes.

You don't need to be technical. You'll never write code. The slash commands handle everything.

---

## Step 1 — Install the plugin

Open Claude Code desktop. In any chat, paste:

> Please add `https://github.com/kaanayaz/agency-starter` as a Claude Code marketplace and install the agency-starter plugin from it.

Claude will ask for permission to install — click **Allow**. After it confirms, **fully quit and restart Claude Code** (Cmd+Q on Mac, then reopen). The restart is needed for the new plugin to load cleanly.

When Claude Code is back open, type:

```
/start
```

`/start` should print a setup checklist. If it does, you're set. (No Terminal, no JSON editing — Claude handles the install for you.)

---

## Step 2 — Install the Claude in Chrome extension

Several setup steps walk you through web flows (creating your Slack app, your Notion integration). Claude in Chrome guides you through them on the page itself.

1. Go to https://claude.ai/download
2. Install the Chrome extension
3. Sign in with the same account you use for Claude Code

---

## Step 3 — Type `/start` (in any language)

Open a new Claude Code chat and type:

```
/start
```

You can type it in any language — `/start`, `/başla`, `/iniciar` all work the same. The first thing the system does is ask what language you want it to use. Pick once; it remembers. (Slack drafts, deck copy, and outreach get their own language setting during discovery — set per-client overrides later if needed.)

Claude detects what's set up, what's missing, and walks you through everything else. The setup commands you'll be guided through, in order:

| Command | What it does | Time |
|---|---|---|
| `/setup-mcps` | Connect Claude to Notion, Slack, Gmail, and Google Drive | ~10 min |
| `/setup-slack` | Walks you through creating your Slack app and `#ops` channel | ~15 min |
| `/setup-notion` | Builds your Agency Ops workspace (7 databases) in Notion | ~5 min |
| `/setup-discovery` | Interview that fills in your team, brand voice, and tools | ~30 min |
| `/setup-smoke-test` | Verifies everything is wired end-to-end | ~2 min |
| `/first-task` | Walks you through your first real task with Claude, then saves it as a one-click command for next time | ~30 min |
| `/import-cowork` | (optional) If you've been using Claude Cowork, point this at your export and the system will mine your past sessions for tasks, rules, and reference data worth saving | ~15 min |

You can pause and resume at any time. Each command is idempotent — if you've already done part of it, re-running picks up where you left off.

---

## When something breaks

Type `/setup-help`. It captures what you were doing and emails us from your own Gmail account. We typically respond within a working day.

Don't paste any tokens or passwords into the chat — `/setup-help` strips those automatically, but the safer move is not to paste them in the first place.

---

## What you get out of it

By the end of Step 3:

- Your Notion has a complete operations workspace your team can edit directly
- Your Slack has a channel where Claude posts drafts for your review
- Your first repetitive task is now a `/<task-name>` command you can re-run any time
- Claude will start noticing patterns across your sessions and asking if you want to save them as shortcuts (you say yes or no — no setup required)

By week 4, you'll have ~10 of these one-click commands and the system will start running scheduled work on its own — drafting your weekly report on Mondays, queuing your invoice review on Wednesdays, etc. — always pausing for your approval before sending anything externally.

Welcome aboard.
