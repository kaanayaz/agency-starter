# Setting up your Notion workspace

This is the place that holds your team's institutional knowledge — what your agency does, who works on what, what the brand sounds like, and the running list of tasks the agents are working on.

> **Why Notion?** Because you already use it (or can within an hour), agents can read and write through the Notion MCP, and editing a page is friendlier than editing a markdown file in a git repo.

---

## Step 1 — Duplicate the template

We'll send you a single Notion template link. In Notion:

1. Open the link
2. Click **Duplicate** (top right)
3. Pick the workspace you want it in
4. Wait ~30 seconds for the copy to finish

You should now have a new page in your sidebar called **🤖 Agency Ops** with seven sub-pages.

---

## Step 2 — The seven databases

Every database is pre-structured. You'll add your own rows during onboarding (step 6 of `ONBOARDING.md`).

### 1. **Team**
Rows: one per teammate.
Properties: Name, Role, Email, Slack User ID, Working Hours (timezone-aware), Default Owner For (multi-select: invoices, decks, finance, outreach, etc.), Approval Tier (auto-approve / always-review).

The **Slack User ID** matters — it's how agents `<@mention>` the right person in `#ops`.

### 2. **Brand Voice**
Plain page (not a database). Sections:
- Tone (3-5 adjectives)
- Always say
- Never say
- Signature phrases / openers / closers
- Email signature template
- Voice exemplars (links to 3-5 emails or messages that nail the tone)

This page is loaded by every writing agent (outreach, follow-ups, deck copy) before producing output.

### 3. **Entities**
One row per "thing the agency uses or sells":
- Tools (invoice system, CRM, ad platforms, video editor, etc.) — name, login URL, who owns it, has-API-yes-or-no
- Service tiers (the products you sell to your clients)
- Client roster shape (what fields you track per client — relevant for the deck builder and reports)

### 4. **Agent Todos**
The shared queue between agents and humans.
Properties: Title, Owner Agent, Owner Human (linked from Team), Status (pending / in-progress / done / blocked), Tier (routine / acceptable / critical), Due, Notes, Created By.

This is the most-read database in the system. Agents read it on every run; humans clear items as they're done. Cleared items stay 7 days then auto-archive (manual setting in Notion you'll configure).

### 5. **Learnings**
Two sub-tabs:

- **Per-agent learnings** — corrections, patterns, "always do X" rules per agent
- **Cross-agent signals** — observations one agent made that another should know

Format: each entry has a date, the agent, the observation, and a "promotion status" (Log → Active Insight → Graduated to Brand/Entities). The pattern matches buzzfy/sevde — Log entries get pruned every 30 days; insights seen 3+ times get promoted.

### 6. **Run Log**
The Orchestrator writes one row per scheduled run. Properties: timestamp, hour (local), agents dispatched, todos pinged, status (ok/partial/check-only), notes.

You don't write here. Read it when something seems off — it's your audit trail.

### 7. **Schedule**
Controls when each agent runs.
Properties: Agent, Mode, Run Hours (multi-select: 09, 12, 15, 18, 21, 00 in your local time), Days (multi-select: Mon..Sun), Status (active / paused / draft), Owner.

The Orchestrator reads this every run and dispatches agents whose row matches the current hour + day + has `status: active`.

---

## Step 3 — Create a Notion integration

Required so Claude can read/write your pages.

1. Go to https://www.notion.so/profile/integrations
2. Click **New integration**
3. Name it: `Agency Bot`
4. Type: `Internal`
5. Capabilities — check **Read content**, **Update content**, **Insert content**
6. Click **Save**
7. Copy the **Internal Integration Secret** (starts with `ntn_` or similar)

---

## Step 4 — Connect the integration to your Agency Ops page

Critical step that's easy to forget:

1. Open the **🤖 Agency Ops** page in Notion
2. Click the `•••` menu top right
3. Click **Connections** → **Connect to** → search for `Agency Bot` → click it

This grants the integration access to that page **and all sub-pages**. Without this, Claude will get "not found" errors trying to read your databases.

---

## Step 5 — Give Claude the integration token

```bash
claude --set-env NOTION_TOKEN=ntn_...
```

Verify:

```bash
echo $NOTION_TOKEN | cut -c1-4    # should print "ntn_"
```

---

## Step 6 — Smoke test

In a Claude Code session:

```
List the databases in our Agency Ops Notion workspace.
```

Claude should return all seven. If you see "no pages found" — redo step 4.

---

## Permissions tip

The integration we just created has access **only to the Agency Ops page and its descendants**. It cannot see other pages in your Notion workspace. If you later want an agent to read a client deck or a meeting note, you have to explicitly **Connect** the integration to that page too.

This is intentional. Limits blast radius if a prompt goes wrong.

---

## What lives in Notion vs what lives in the plugin

A common confusion. The split:

| In Notion (you edit) | In the plugin (we maintain) |
|---|---|
| Team, Brand Voice, Entities | Agent prompts (the "instructions" each agent follows) |
| Agent Todos, Run Log, Learnings | Slash commands (`/codify`, `/promote`, `/<your-codified-tasks>`) |
| Schedule (when agents run) | Skills (reusable building blocks: send-slack-message, draft-email, etc.) |
| Concepts, playbook drafts | Orchestrator dispatch logic |

If you ever want to **change what an agent does**, that's a plugin change (we do it). If you want to **change when an agent runs, who owns what, or what the brand sounds like**, that's a Notion change (you do it).
