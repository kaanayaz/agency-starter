---
name: first-task
description: Guide your first real task with Claude, then codify it into a reusable slash command.
---

You are walking the operator through their first real task. They've finished setup; this is the first time they actually use Claude for work. The goal isn't just to do the task — it's to do it in a way that produces a clean `/codify` afterward, so the second time they do this task it's one command.

This command is the bridge between "Claude is set up" and "Claude is part of how the agency works."

# Step 0 — Frame it

Print:

> Pick a task you'd normally do today — something repetitive enough that you'd want to automate it eventually. Examples: drafting a follow-up email after a sales call, building a weekly report from a spreadsheet, processing a batch of invoices, sourcing creators for a brief.
>
> We'll do it together. You drive — I'll watch, fetch what you need from your tools, and at the end I'll codify it into a `/<task-name>` command you can re-run later.

Then ask: *"What task are you about to do? One sentence."*

Wait for their answer.

# Step 1 — Acknowledge and prepare

Acknowledge briefly (one sentence — don't lecture). Then:

1. **Confirm the task is a good `/codify` candidate.** Bad candidates:
   - Truly one-off work (a unique strategic decision, a personal note)
   - Already automated elsewhere (e.g. a HubSpot workflow handles this)
   - Requires judgment that's different every time (creative direction)
   - If you suspect bad fit, gently ask: *"Is this something you'd do at least every week or two? If not, we can still do it together, but it might not be worth codifying."*
2. **Quick context pull.** What does the operator need fetched? Pull it now. Examples:
   - Brand Voice page (if writing)
   - Team DB (if pinging)
   - The relevant client's row (if client-specific)
3. **Set expectations.** *"I'll stay quiet during the work unless you ask. When you're done, just say `done` or `let's codify`."*

# Step 2 — Do the work

Operate in normal Claude mode. The operator drives. You:

- Fetch from MCPs when asked
- Draft when asked
- Don't volunteer optimizations during the run — the goal is to capture what they actually do, not what they should do
- Don't push them toward a "better" workflow — wrong shape for the codified version
- **Pause for explicit approval before any external action** (sending email, posting to Slack outside `#ops`, marking external state changed). External actions go through Gmail Drafts / pinned Slack messages first

# Step 3 — Watch for codification triggers

The operator may signal completion in several ways:

- *"Done"* / *"That's it"* / *"Finished"*
- *"Codify this"* / *"Save this"* / *"Make this a command"*
- A natural pause where they stop asking for things

If unsure whether they're done, ask once: *"Looks like that wraps it. Want to codify now, or are there more steps?"*

# Step 4 — Codify

Invoke the `/codify` slash command via the SlashCommand tool. `/codify` already knows what to do — it reads the session, asks the slug + inputs questions, and drops a draft command.

After `/codify` finishes, add one line of your own:

> Drafted. Try running `/<slug>` next time the same task comes up. After 3 successful runs it graduates to `tested`; after 8 to `stable`. Only `stable` commands get auto-dispatched by the Orchestrator on a schedule.

# Step 5 — Set the next expectation

Print:

> That's your first codified task. The rhythm from here:
>
> 1. Use `/<slug>` when the task comes up again.
> 2. Light corrections each time — those become permanent rules.
> 3. After 8 runs it's stable. We can schedule it.
>
> When you're ready to do task #2, just type `/first-task` again — same flow, new task.

End cleanly.

# Anti-overreach rules

- **You are an observer here, not a co-driver.** Resist optimizing the operator's workflow during the run. The codified version captures what *they* did — if you reshape it, the codified version is yours, not theirs, and it'll feel foreign on first re-run.
- **Don't bake assumptions in.** If the operator did something specific to today (a particular client, a particular date), `/codify` is responsible for replacing those with `<input>` placeholders. Don't preempt.
- **One task per session.** If the operator finishes one task and starts another in the same session, ask: *"That's a separate task — should I codify the first one before we start the second?"* Multi-task sessions produce muddled drafts.
- **Don't volunteer the noticer.** The pattern-recognizer skill runs on its own (via the post-session hook). You don't need to tell the operator about it during `/first-task`.
