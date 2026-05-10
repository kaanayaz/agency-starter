---
name: codify
description: Convert the current chat session into a draft slash command the operator can re-run later.
---

You are converting the current Claude Code session into a reusable slash command. The operator just finished a real task with you and wants to capture how it went so future runs are one-shot.

# Your job

1. **Review the session.** Skim the conversation that led to this `/codify` call. Identify:
   - The actual goal the operator was trying to accomplish (in their words, not yours)
   - The tools and MCPs that got used (Notion / Gmail / Drive / Slack / Bash / etc.)
   - The inputs the operator provided (files, links, freeform context)
   - The decision points where the operator overrode you or corrected something — these become explicit rules in the codified version
   - The external actions that succeeded vs. were drafted-but-not-sent
   - Anything that was *specific to this session* (a particular client name, a particular date) vs. *general to the task* (the shape of the work)

2. **Ask the operator three short questions:**
   - **Slug?** Suggest one based on the goal (e.g. `approve-invoices`, `creator-outreach`, `monthly-finance-report`). Confirm or accept their override. Use kebab-case.
   - **What changes between runs?** This is what becomes the command's input. Examples: which client, which month, which creator list. List 1–3 inputs.
   - **What stays the same?** This is the part that becomes hardcoded in the prompt. Brand voice rules, approval gates, the order of steps.

3. **Draft the command file** at `~/.claude/commands/drafts/<slug>.md` with this shape:

```markdown
---
name: <slug>
description: <one-line description, written by you, accepted by operator>
stability: draft
run_count: 0
required_for_tested: 3
required_for_stable: 8
codified_at: <ISO timestamp>
codified_from_session: <session id if available, else "manual">
inputs:
  - name: <input1>
    description: <what this is>
  - name: <input2>
    description: <what this is>
last_runs: []
---

# <Goal in operator's words>

You are helping the operator <accomplish the goal>. They invoked you with `/<slug>`. The inputs they provided are listed above; ask for any that are missing before starting.

## Steps

1. <Step 1 — exact action that happened in the codified session, generalized>
2. <Step 2 — etc.>
...

## Rules baked in from the original session

- <Rule 1 — usually a correction the operator made>
- <Rule 2>
...

## Default mode: prepare

External actions (sending email, posting to Slack outside `#ops`, marking external state changed) require an explicit operator approval at each step. Draft into Notion / Gmail Drafts / pinned Slack messages and pause for review.

## Logging this run

After the task completes (success or partial), append one line to `~/.claude/agency-starter/usage.jsonl`:

\`\`\`json
{"command": "<slug>", "ts": "<ISO>", "outcome": "ok|partial|aborted", "notes": "<short>"}
\`\`\`

This is what `/promote` reads to decide stability transitions.
```

4. **Show the operator the draft path** and tell them:

   > Drafted `/<slug>` at `~/.claude/commands/drafts/<slug>.md` (stability: draft, run_count: 0).
   >
   > Run it 2 more times before it graduates to `tested`. Run it 8 times total before `stable`.
   > Only `stable` commands can be auto-dispatched by the Orchestrator.
   >
   > After each run, the command logs to `~/.claude/agency-starter/usage.jsonl`. When the threshold is hit, run `/promote <slug>` (or it auto-promotes if `auto-promote` is enabled in plugin config).

5. **Do not move the file out of `drafts/`.** That's `/promote`'s job.

# Anti-overfitting rules

The biggest failure mode here is the draft codifying *this* session's specifics rather than the general task. Mitigations:

- **Replace concrete client names with `<input>` placeholders.** If the operator says "do this for ACME Corp," `<input: client_name>` belongs in the command, not "ACME Corp".
- **Replace concrete dates with relative dates.** "May 2026 invoices" → `<input: month>` or `current month`.
- **If the operator made the same correction more than once in the session, that's a hard rule.** Bake it in.
- **If the operator made a correction once, surface it as a question on first run** — don't bake it in yet.
- **Flag uncertainty.** End the draft with a "Known unknowns" comment listing things you weren't sure how to generalize. The operator decides on the next run.

# What success looks like

A draft so close to the original session that the operator's first re-run feels familiar, with explicit hooks for the inputs that vary. They run it twice more on different inputs, light corrections each time, and by run 4 they barely think about it.

# What failure looks like

A draft so generic it's useless ("draft an email about something"). Or so specific it only works once. Both are pushed back on by the operator on first re-run, which is fine — that's what `tested` exists for.
