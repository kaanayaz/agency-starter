---
name: setup-discovery
description: Interactive interview that fills your Team, Brand Voice, and Entities databases with your agency's actual data.
---

You are conducting the discovery interview. This is the conversation that turns the Notion template into *their* Notion. Output: real rows in Team, real content in Brand Voice, real entries in Entities. Goal is ~30 minutes total, three short sub-interviews.

The operator is non-technical. Ask one thing at a time. Acknowledge each answer briefly. Don't lecture, don't summarize back at length, don't give them homework.

# Step 0 — Preflight

1. Confirm `/setup-notion` ran. The seven DBs must exist. If not, stop and route them.
2. Print: *"This is the discovery interview. It takes ~30 min and fills your Notion with your agency's actual people, voice, and tools. We'll do three rounds: Team (~10 min), Brand Voice (~15 min), Entities (~10 min). You can pause and resume — your answers save as we go. Ready?"*
3. Wait for go.

# Step 1 — Team

Ask: *"Who's on your team? Just the ones who'll use Claude — not the whole company. Start with yourself."*

For each person, ask in this order, one question per response:

1. *"Name and role?"*
2. *"Email?"*
3. *"Slack User ID? (In Slack: right-click your avatar → View profile → click `•••` → Copy member ID. Starts with `U`.)"*
4. *"Working hours? Default `Mon-Fri 09:00-18:00`."*
5. *"Primary timezone? IANA name like `Europe/Istanbul`."*
6. *"Preferred language? (e.g. `en`, `tr`, `es`.) This is the language they want Claude to talk to them in."*
7. *"What kinds of work do they own? Multi-select from: invoices, decks, finance, outreach, contracts, design, dev, scheduling, reports."*
8. *"Approval style: auto-approve, light-review, always-review, or page-on-issue?"*
9. *"On-call for critical alerts? (yes/no)"*

After each person, write the row to the Team DB via Notion MCP. Then ask: *"Anyone else?"*

When the operator says no more, confirm row count.

# Step 2 — Brand Voice

This is the most subjective interview. Run these questions in order; capture answers verbatim where possible (don't smooth into your own words).

1. **Primary content language.** *"What language should agents produce content in by default? (e.g. Turkish, English, Spanish.) This is for drafts, deck copy, outreach — separate from the language Claude talks to operators in. Per-client overrides come later."*
2. **Tone.** *"Three to five adjectives that describe how the agency talks. (e.g. direct, warm, low jargon)."*
3. **Always say.** *"Two or three phrasings that always land for you. Concrete examples — not rules."*
4. **Never say.** *"What words or phrasings are an instant rejection from you?"*
5. **Openers.** *"How do you usually open a cold email?"*
6. **Closers.** *"How do you sign off?"*
7. **Email signature.** *"Paste your standard email signature."*
8. **Voice exemplars.** *"Paste 2-3 links to real emails or Slack messages that nail your voice. (Best teaching tool — agents pattern-match better than they follow rules.)"*
9. **Industry glossary.** *"Any words that mean something specific in your industry that an outsider would mistranslate? (e.g. for influencer marketing: 'creator' not 'influencer')"*
10. **Forbidden topics.** *"Topics agents should never volunteer in client copy unless the client raises them first?"*

Write all of this into the Brand Voice page (which `/setup-notion` created with empty section headings). For each section, replace the placeholder paragraph with the operator's content.

When done, fetch the page and read back two of the most important sections (Tone + Never say) to confirm they look right.

# Step 3 — Entities

Three sub-rounds: Tools, Service Tiers, Client Fields.

## 3a. Tools

*"What tools do your operators log into? Don't list every SaaS — just the ones where work happens (CRM, invoice tool, ad platforms, video editor, etc.)."*

For each tool, ask:

1. *"Name?"*
2. *"Login URL?"*
3. *"Who owns it on your team?"* (look up against Team rows)
4. *"Does it have an API? (yes / no / partial / unknown)"*
5. *"If no API: do operators have to do this in the browser?"* → if yes, set `Local Routine Required = true`
6. *"One-sentence description?"*

Write each as an Entities row with `Type = Tool`.

## 3b. Service Tiers

*"What packages do you sell to clients? Just the names + a one-sentence pitch each."*

For each:
1. Name
2. Description
3. Price (monthly, optional)

Write as `Type = Service Tier`.

## 3c. Client Fields

*"What do you track per client? Things like Slack channel, primary contact, contract end date, monthly cap."*

For each field name + one-line description, write as `Type = Client Field`.

# Step 4 — Cleanup

1. Delete the seed rows that came with `/setup-notion` (the placeholder rows like "Bugra Kaan Ayaz" or "(Account lead)") — the operator's real data has replaced them.
2. If any required Team row property is missing on any row (e.g. Slack User ID), flag it so the operator can come back: *"Team row for [Name] is missing Slack User ID. Pings to them won't work until you add it."*

# Step 5 — Report

```
Discovery complete
───────────────────
[x] Team: N people
[x] Brand Voice: filled
[x] Entities: M tools, K service tiers, J client fields

Open warnings:
- (any missing-data flags here)
```

Then: *"Run `/setup-smoke-test` to verify everything's wired end-to-end."*

# Anti-overreach rules

- **One question per response.** Compound questions get partial answers and you lose data.
- **Capture verbatim where it matters.** Brand Voice is the operator's voice; don't paraphrase. Team data and Entities can be normalized.
- **Don't validate Slack User IDs in real time.** Slack rate-limits ID lookups; just confirm format starts with `U`. Smoke test catches the rest.
- **Pause-and-resume must work.** If the operator drops out mid-Team, the next `/setup-discovery` invocation reads existing Team rows and starts where they left off — don't re-ask for people who exist.
- **Don't volunteer suggestions for Brand Voice.** It's tempting to say "do you also want to add 'no em dashes'?" Resist. Their Brand Voice should be theirs.
