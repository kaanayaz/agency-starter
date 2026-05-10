---
name: promote
description: Promote a codified command from draft → tested → stable based on accumulated runs.
---

You are managing the stability ladder for codified commands. Only `stable` commands can be auto-dispatched by the Orchestrator on a schedule, so this is the gate that decides what runs unattended.

# Inputs

The operator invokes you as `/promote <slug>` (e.g. `/promote approve-invoices`). If no slug is provided, list all draft + tested commands with their run counts and ask which one.

# Stability ladder

```
draft   → tested  : requires ≥ run_count.required_for_tested distinct runs (default 3) with outcome "ok"
tested  → stable  : requires ≥ run_count.required_for_stable distinct runs (default 8) with outcome "ok"
```

"Distinct runs" means ≥3 different sets of inputs. Three runs with the *same* invoice list is one run, not three. The operator's judgment overrides this if they want to push back.

# Your job

1. **Locate the command file.** It's in `~/.claude/commands/drafts/<slug>.md` (draft) or `~/.claude/commands/<slug>.md` (tested). If neither exists, tell the operator and exit.

2. **Read the usage log.** `~/.claude/agency-starter/usage.jsonl` — one JSON line per run. Filter to entries where `command == <slug>`.

3. **Compute readiness:**
   - `total_runs` = count of entries
   - `ok_runs` = count where `outcome == "ok"`
   - `distinct_runs` = count of unique input-fingerprints (heuristic: hash the `notes` field; if `notes` is empty for ≥half of runs, prompt the operator to confirm distinctness manually)

4. **Decide the action:**

   **Promote draft → tested:**
   - `stability: draft` AND `ok_runs ≥ required_for_tested` AND `distinct_runs ≥ required_for_tested`
   - Move file from `drafts/` to `commands/`
   - Update frontmatter: `stability: tested`, `promoted_to_tested_at: <ISO>`
   - Show the operator: *"Promoted `/<slug>` to `tested`. It can now run with light human oversight. Schedule it in Notion's Schedule DB if you want recurring runs (still operator-driven). To graduate to `stable`, accumulate {required_for_stable - ok_runs} more successful runs."*

   **Promote tested → stable:**
   - `stability: tested` AND `ok_runs ≥ required_for_stable` AND `distinct_runs ≥ required_for_stable`
   - Update frontmatter: `stability: stable`, `promoted_to_stable_at: <ISO>`
   - Show the operator: *"Promoted `/<slug>` to `stable`. The Orchestrator can now dispatch this on schedule. Add it to Notion's Schedule DB with `Status: active` to enable."*

   **Not yet ready:**
   - Show the operator a status line:
     ```
     /<slug> is at <current_stability>.
     Runs: <ok_runs>/<required> ok · <distinct_runs>/<required> distinct
     Recent outcomes: ok ok partial ok ...
     Needed: <delta> more ok-and-distinct runs to graduate.
     ```
   - Highlight if the recent outcomes are trending toward `partial` or `aborted` — that's a sign the command needs editing, not promotion.

   **Demote (rare but allowed):**
   - If the operator passes `/promote <slug> --demote`, move it down one rung and clear the runs that occurred at the higher rung. Use case: a `tested` command started failing after an external API change; demote it to `draft` while you fix the prompt.

5. **Log the promotion** to `~/.claude/agency-starter/promotions.jsonl`:

   ```json
   {"command": "<slug>", "from": "<old>", "to": "<new>", "ts": "<ISO>", "ok_runs": N, "distinct_runs": N}
   ```

# Auto-promotion

If the plugin config has `auto_promote: true`, the codified commands themselves call `/promote <slug>` after they finish a run, instead of the operator doing it manually. Default is **false** — we want the operator in the loop for the first few promotions of every command.

# Anti-rubber-stamping rules

- **Distinct runs matter more than total runs.** If the operator runs the same command on the same client 8 times, that's not 8 runs — that's 1.
- **Watch for `partial` clusters.** If the last 3 runs are all `partial`, refuse to promote and tell the operator: *"The command's recent runs are degrading. Edit the prompt or `/codify` a new version before promoting."*
- **Don't auto-promote across stability boundaries.** Even with `auto_promote: true`, the jump from `tested` to `stable` should require an explicit operator confirmation, because that's the point where the Orchestrator can dispatch it unattended.

# What this gives you over time

A library that sorts itself. New ideas land as `draft` and most get retired without making it past `tested` — that's a feature, not a bug. The handful that make `stable` are the ones the agency actually depends on, and the Orchestrator runs them on schedule with the operator's confidence behind them.
