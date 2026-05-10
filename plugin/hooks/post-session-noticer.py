#!/usr/bin/env python3
# Stop hook for agency-starter.
#
# Reads the just-completed Claude Code session, looks for two cheap-to-detect
# trigger patterns (standing-rule phrases and missing-tool reaches), and queues
# any matches to ~/.claude/agency-starter/noticer-queue.jsonl.
#
# The cross-session noticer (Orchestrator Step 5b) handles the harder patterns
# (repeat-task, repeat-correction, repeat-reference) that need cross-session view.
#
# Wiring: registered via plugin/.claude-plugin/hooks.json on the Stop event.
# If the plugin manifest doesn't auto-wire, /start detects and offers to add
# the snippet to ~/.claude/settings.json.
#
# Input (stdin): JSON object with keys including `session_id`, `transcript_path`
# or `transcript`. Schema follows Claude Code's Stop hook contract.
# Output (stdout): a one-line notice if any suggestions were queued. Silent if
# nothing matched. Never errors loudly — a hook crash should never block the
# session.

import json
import re
import sys
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

QUEUE_DIR = Path.home() / ".claude" / "agency-starter"
QUEUE_PATH = QUEUE_DIR / "noticer-queue.jsonl"
REJECTED_PATH = QUEUE_DIR / "noticer-rejected.jsonl"

STANDING_RULE_PATTERNS = [
    r"\b(every time|from now on|always|never|next time|whenever|each time)\b",
]

MISSING_TOOL_PATTERNS = [
    r"(?i)i (don't|do not|can't|cannot)\s+(have access to|connect to|reach|read|see)\s+([a-zA-Z][\w\s]{0,30})",
    r"(?i)there (is|isn't|is no|isn't a)\s+(mcp|integration|connection)\s+for\s+([a-zA-Z][\w\s]{0,30})",
]


def load_transcript(event):
    if isinstance(event.get("transcript"), str) and event["transcript"]:
        return event["transcript"]
    path = event.get("transcript_path")
    if path:
        try:
            return Path(path).read_text(errors="ignore")
        except (OSError, IOError):
            return ""
    return ""


def load_rejected_fingerprints():
    if not REJECTED_PATH.exists():
        return set()
    fingerprints = set()
    try:
        for line in REJECTED_PATH.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                fp = entry.get("fingerprint")
                if fp:
                    fingerprints.add(fp)
            except json.JSONDecodeError:
                continue
    except (OSError, IOError):
        pass
    return fingerprints


def fingerprint(suggestion_type, payload):
    h = sha256()
    h.update(suggestion_type.encode())
    h.update(b"|")
    h.update(payload.encode())
    return h.hexdigest()[:16]


def extract_sentence_around(text, span_start, span_end, max_len=200):
    start = text.rfind(".", 0, span_start) + 1
    if start <= 0:
        start = max(0, span_start - 80)
    end = text.find(".", span_end)
    if end < 0:
        end = min(len(text), span_end + 120)
    quote = text[start:end].strip()
    return quote[:max_len]


def find_standing_rules(transcript, rejected):
    out = []
    for pat in STANDING_RULE_PATTERNS:
        for match in re.finditer(pat, transcript, re.IGNORECASE):
            quote = extract_sentence_around(transcript, match.start(), match.end())
            if not quote:
                continue
            fp = fingerprint("standing-rule", quote)
            if fp in rejected:
                continue
            out.append({"type": "standing-rule", "quote": quote, "fingerprint": fp})
            break  # one per session for this category
        if out:
            break
    return out


def find_missing_tool(transcript, rejected):
    for pat in MISSING_TOOL_PATTERNS:
        match = re.search(pat, transcript)
        if not match:
            continue
        # group(3) captured the tool name in both patterns
        try:
            tool = match.group(3).strip()
        except IndexError:
            continue
        if not tool or len(tool) > 40:
            continue
        fp = fingerprint("missing-tool", tool.lower())
        if fp in rejected:
            continue
        return [{"type": "missing-tool", "tool": tool, "fingerprint": fp}]
    return []


def main():
    try:
        raw = sys.stdin.read()
        event = json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    transcript = load_transcript(event)
    if not transcript:
        sys.exit(0)

    rejected = load_rejected_fingerprints()

    suggestions = []
    suggestions.extend(find_standing_rules(transcript, rejected))
    suggestions.extend(find_missing_tool(transcript, rejected))

    if not suggestions:
        sys.exit(0)

    # Cap to one per session — the strongest one wins (standing-rule beats missing-tool)
    suggestions = suggestions[:1]

    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    session_id = event.get("session_id", "unknown")

    try:
        with QUEUE_PATH.open("a") as f:
            for s in suggestions:
                entry = {"ts": now, "session_id": session_id, **s}
                f.write(json.dumps(entry) + "\n")
    except (OSError, IOError):
        sys.exit(0)

    n = len(suggestions)
    label = "suggestion" if n == 1 else "suggestions"
    print(f"Noticer: queued {n} {label}. Type /start to review.")


if __name__ == "__main__":
    main()
