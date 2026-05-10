# agency-starter

Internal scaffold for delivering a Claude-powered ops layer to non-technical agencies.

> **Audience for this README:** us (Bugra + future maintainers). Everything client-facing is in `ONBOARDING.md` and `docs/`.

## What this is

A reusable starter kit that turns a non-technical agency (initial target: an influencer marketing agency) into a Claude-augmented one without making them learn git, markdown wiki conventions, or write prompts.

It is **not** a port of `buzzfy/wiki/` to a different folder. The buzzfy/sevde pattern assumes the operator is technical, lives in GitHub, reads PRs, and writes Markdown. This audience does none of those things.

## What stays from buzzfy/sevde

- One **Orchestrator** routine that dispatches many agents per run
- A schedule file the orchestrator reads
- Per-agent personas in Slack with avatars + Block Kit posts
- Self-learning + feedback relay via thread replies
- An `agent-todos` shared queue between agents and humans
- Owner routing via a team roster

## What changes

| buzzfy / sevde | agency-starter |
|---|---|
| Wiki in `wiki/*.md` in a GitHub repo | Wiki in **Notion** (DBs they edit directly) |
| Prompts in `wiki/agents/<name>.md` (git) | Agent prompts in this **plugin repo** (we maintain) |
| Agents push to branches, PRs auto-merge | Agents write back to Notion + draft Gmail/Slack |
| Operator reads PRs / commits | Operator reads Notion + Slack only |
| All routines cloud (CCR) | **Cloud + local** split — local routines for browser-bound tasks (e.g. Turkish invoice tools without APIs) |
| Agents are the only abstraction | **Agents + skills + slash commands**, with a `/codify` graduation loop from manual sessions |
| Default mode: agents act | Default mode: **agent prepares, human approves** |

## Repo shape

```
agency-starter/
├── README.md                # ← you are here (internal)
├── ONBOARDING.md            # client-facing onboarding checklist
├── docs/
│   ├── slack-setup.md       # how the agency creates their Slack app
│   ├── notion-setup.md      # how to clone the Notion templates
│   └── architecture.md      # one-pager for technical hand-off (optional reading for them)
├── notion-templates/        # markdown source-of-truth for Notion DBs we'll create in their workspace
└── plugin/                  # the Claude Code plugin we install on each operator's machine
    ├── .claude-plugin/
    │   └── plugin.json
    ├── agents/              # cloud + local agent prompts (read by Orchestrator)
    │   └── orchestrator.md  # the dispatcher
    ├── commands/            # slash commands for operators
    │   ├── codify.md        # convert a manual session into a draft slash command
    │   └── promote.md       # graduate a draft → tested → stable
    ├── skills/              # reusable skills agents and operators can call
    └── playbooks/           # opinionated recipes (deck templates, outreach scripts, etc.)
```

## Delivery model

1. **Discovery (60–90 min)** — interview the agency: tools, tasks, owners, invoice tool name, CRM location.
2. **Setup (we do most of it with them on a call)**:
   - Install Claude Code on each operator's Mac
   - Connect required MCPs (Notion, Gmail, Drive, Slack)
   - Create their Slack app per `docs/slack-setup.md` (we walk them through; this is also the moment they level up)
   - Clone Notion templates into their workspace per `docs/notion-setup.md`
   - Install this plugin (`claude plugins install <private-repo>`)
3. **First sprint (week 1)** — pair on 2–3 manual tasks per operator, run `/codify` after each, end the week with a small library of `draft` commands.
4. **Maturation (weeks 2–4)** — operators run their drafts, `/promote` flips stability as runs accumulate, the Orchestrator gradually picks up scheduled work.
5. **Hand-off** — they own their Notion + their plugin. We support via Slack / occasional pairing.

## Stability ladder (the `/codify` graduation idea)

Every command drafted by `/codify` carries frontmatter:

```yaml
stability: draft       # draft → tested → stable
run_count: 0           # auto-incremented on each invocation
required_for_tested: 3
required_for_stable: 8
```

- **draft** — created by `/codify`, never run unattended; always paired with the operator.
- **tested** — survived ≥3 distinct runs (different inputs / contexts), can run with light human oversight.
- **stable** — survived ≥8 runs, eligible to be invoked by an Orchestrator routine.

The **Orchestrator only dispatches `stable` commands automatically.** Draft and tested live in the operator's manual workflow. This is the safety rail against `/codify` overfitting to a single session.

## Open design questions

- **Sync mechanism for the plugin** — do we deliver as a git-backed Claude Code plugin (simplest, but each operator gets updates via `claude plugins update`), or as a private MCP that serves prompts from a hosted source? Default: plugin.
- **Where does `run_count` live?** Local file per operator (drift between machines), Notion (single source but write-heavy), or both with reconciliation? Default: local file, Notion is the read model for promotion.
- **Slack app per agency or shared?** Each agency creates their own — shared would leak data and confuse permissions.
- **Browser-bound local routines** — `mcp__scheduled-tasks__*` is fine but only fires when Claude Code is open. Need to decide if we accept that constraint or wire `cron` + headless Claude Code. Default: accept the constraint, document it.

## Status

Scaffold only. No client deployed yet.
