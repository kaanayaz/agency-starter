# Brand Voice

A **plain Notion page** (not a database). Every writing agent — outreach, follow-ups, deck copy, invoice replies, ad creatives — loads this page in full before producing output.

Treat it as the agency's stylebook. Update it when you notice a draft that didn't sound like you — that's the signal something's missing here.

## Page structure

Use Notion `Heading 2` blocks for each section header below. Keep entries scannable; long prose dilutes signal.

### Primary Language

The default language for all agent-produced content (drafts, deck copy, outreach, invoice replies). Operators may type slash commands and questions in any language; this is the language *the output* lands in.

- **Default:** specify here (e.g. `Turkish (tr)`, `English (en)`, `Spanish (es)`)
- **Per-client overrides:** if a specific client wants comms in a different language, add a `Language Override` field to that client's row in Entities (Type = Client Field). Agents check the per-client override before falling back to this default.
- **Mixed-language sources are fine.** If you brief in English but the client wants Turkish output, agents handle the translation.

### Tone

Three to five adjectives that describe how the agency talks. Examples (replace with yours):

- Direct
- Warm-but-professional
- Confident, never salesy
- Low jargon, high specificity

### Always say

Phrasings that always land. Each entry is a one-liner with a tiny example.

- Use specific numbers ("47 creators" not "many creators")
- Lead with the result, then the method
- Name the client by their first name in subject lines
- "We" when describing the agency, "I" when the operator is the named author

### Never say

The instant-rejection list. If a draft has any of these, it's wrong.

- "Just checking in"
- Hedging openers: "Sorry to bother you", "I know you're busy"
- Hyperbolic claims without proof ("revolutionary", "game-changing")
- Apologies for following up if no commitment was missed
- Buzzwords: "synergy", "leverage" (verb), "circle back", "touch base"

### Signature phrases / openers / closers

Phrases the team genuinely uses and that should appear in agent drafts to keep voice consistent.

- Openers: `Quick one —`, `Following our call —`
- Closers: `Speak Friday.`, `Out of curiosity —`
- Bridges: `Worth noting —`, `One thing —`

### Email signature template

The fixed footer that goes on every outbound email draft. Per-operator variants use placeholders:

```
{{first_name}}
{{role}}, {{agency_name}}
{{email}} · {{phone_optional}}
{{agency_url}}
```

### Voice exemplars

Link to 3-5 real emails or Slack messages that nail the voice. Best teaching tool — agents learn the *shape* by example, not by rules alone.

- [Exemplar 1: cold pitch that converted](paste-link)
- [Exemplar 2: follow-up after no-show](paste-link)
- [Exemplar 3: monthly recap to a client](paste-link)
- [Exemplar 4: difficult-news email](paste-link)

### Industry-specific glossary

Words that mean something specific in this industry that an agent might mistranslate. Defaults below assume influencer marketing — replace if the agency operates elsewhere:

- "Creator" not "Influencer" (the audience prefers it)
- "Brief" = the package sent before a campaign, not a short summary
- "UGC" = user-generated content, paid or organic
- "CPC / CPM / CPA" — never spell out, the audience knows
- "Shipping window" = our window to dispatch product, distinct from "delivery window"

### Forbidden topics

Topics agents should never volunteer in client-facing copy unless the client raised them first.

- Pricing speculation
- Competitor names (positive or negative)
- Internal team frustrations
- Technical details of the agent stack itself

## Read contract

- **Loaded by:** every agent that produces written output. This page is concatenated into the agent's system prompt at run start.
- **Written by:** humans only. Agents propose changes by adding rows to **Learnings** with `Promotion Status: Graduated to Brand Voice`.
- **Refresh cadence:** the Orchestrator re-reads on every run, so edits take effect within the next hour.

## Setup pitfalls

- **Page must be inside Agency Ops** for the Notion integration to read it. If you move it, re-share the integration on the new parent.
- **Don't get philosophical.** The "Tone" section is one-liners, not paragraphs. Anything longer dilutes the prompt and the agent under-applies it.
- **Voice exemplars beat rules.** If you have to choose, link more exemplars and write fewer rules. Agents pattern-match better than they follow lists.
- **Update when you reject a draft.** If you killed an outreach draft for tone reasons, the missing rule belongs here, not just in Learnings.
