# Entities

A single database that holds three kinds of "things the agency uses or sells":

1. **Tools** — software the agency or its operators use to deliver work
2. **Service Tiers** — the products/packages the agency sells to clients
3. **Client Fields** — the schema of what fields the agency tracks per client

A `Type` discriminator separates them. Filter by Type to see each as its own view.

## Schema

| Property | Type | Options | Required | Notes |
|---|---|---|---|---|
| Name | Title | — | yes | Display name |
| Type | Select | Tool, Service Tier, Client Field | yes | Drives which other properties matter |
| Description | Text | — | yes | One sentence |
| Login URL | URL | — | conditional | Required if Type = Tool |
| Has API | Select | yes, no, partial, unknown | conditional | Required if Type = Tool. Drives whether automation is cloud or local |
| Local Routine Required | Checkbox | — | conditional | Set when `Has API = no`. Triggers Orchestrator to ping a human via Agent Todos rather than auto-running |
| Owner | Relation → Team | — | yes | Who in the agency owns this thing |
| Vendor | Text | — | conditional | For Tools: who makes it. For Service Tiers: blank |
| Price (Monthly) | Number (currency) | — | conditional | For Tools: subscription cost. For Service Tiers: list price |
| Notes | Text | — | no | Free-form |
| Status | Select | active, deprecated, evaluating | yes | Helps agents avoid suggesting deprecated tools |

### Type-specific guidance

- **Tool** — anything with a login. Examples: invoice tool, CRM, ad platforms, video editor, project tracker. Set `Has API` honestly; `partial` means there's an API but it's missing key endpoints (real-world example: many Turkish e-invoice tools).
- **Service Tier** — the packages the agency sells. Use Notes for what's included; Price (Monthly) is the list price you publish.
- **Client Field** — each row is one *field* you track per client (not one client). Examples: "Slack channel", "Primary contact", "Contract end date", "Monthly cap". The Deck Builder and Reporting agents read this list to know what shape a client record should have.

## Seed rows (replace during discovery)

| Name | Type | Description | Login URL | Has API | Local Routine Required | Owner | Status |
|---|---|---|---|---|---|---|---|
| (Turkish e-invoice tool placeholder) | Tool | Portal where Turkish e-invoices land. No public API; operator works in browser. | https://example.com.tr | no | yes | (Founder) | active |
| HubSpot | Tool | CRM. Pipelines, contacts, deal stages. | https://hubspot.com | yes | no | (Account Manager) | active |
| Meta Ads | Tool | Paid social. | https://business.facebook.com | yes | no | (Account Manager) | active |
| Notion | Tool | This workspace. | https://notion.so | yes | no | (Founder) | active |
| Creator Sourcing — Tier 1 | Service Tier | Up to 10 creators sourced + briefed per month, performance reporting weekly. | — | — | — | (Founder) | active |
| Creator Sourcing — Tier 2 | Service Tier | 10-25 creators, weekly report, monthly strategy review. | — | — | — | (Founder) | active |
| Field: Slack channel | Client Field | The shared channel where day-to-day comms happen for this client. | — | — | — | (Account Manager) | active |
| Field: Monthly cap | Client Field | Spend cap (USD) we won't exceed without explicit approval. | — | — | — | (Account Manager) | active |

## Read/write contract

- **Reads:** every agent that needs context on what tools to use or what tier a client is on; the Orchestrator (to know which tools require local routines vs. cloud)
- **Writes:** humans during onboarding; agents may *propose* additions via Learnings entries with `Promotion Status: Graduated to Entities` (humans approve and move)
- **Change rate:** monthly — when a new tool is added or a service tier changes

## Setup pitfalls

- **`Has API = no` is the routing signal.** The Orchestrator uses it to decide whether work goes cloud-dispatched or queued as a human ping. Get it right or invoice approvals silently fall on the floor.
- **One Type per row.** Don't try to model a tool that's also a service tier — make two rows.
- **Don't dump every Notion page link here.** Entities is for things with operational meaning (logins, APIs, prices). Concept docs live in their own pages.
- **Evaluate vs. deprecated matters.** When a tool is being phased out, set `deprecated` *before* the cutover so agents stop suggesting it during the overlap window.
