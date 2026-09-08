# Musfiraai MCP Server

Live Model Context Protocol server exposing Musfiraai's company info, services,
AI stack, FAQ, reviews, and contact details as tools/resources/prompts for any
MCP-compatible AI client (Claude, GPT, etc).

**Live docs + connect page:** https://dark-spark-uxxux.run.mcp-use.com/
**MCP endpoint:** https://dark-spark-uxxux.run.mcp-use.com/mcp

## Run locally

```
pip install -r requirements.txt
python server.py                                           # stdio (Claude Desktop, local)
MCP_TRANSPORT=streamable-http PORT=8000 python server.py    # HTTP (remote/cloud)
```

## Routes (HTTP mode)
- `GET /` — human-readable docs/landing page (responsive, SEO + FAQ schema)
- `GET /health` — health check
- `POST /mcp` (or `/mcp/`) — the MCP JSON-RPC endpoint
- `GET /build-status?id=MFA-XXXX` — plain JSON status lookup for the website widget

## Free-build status tracking
`request_callback` now returns a `request_id` (e.g. `MFA-4821`) alongside the
email send. Status is stored in the **private** `musfiraai-mcp-guardian` repo
(`data/builds.json`) — never in this public repo, since it holds customer
names/contacts. Requires `GITHUB_TOKEN` (push access to that repo) as an env
var. Status starts at "Received"; moving it to Queued/Building/Delivered is a
manual one-line edit to `data/builds.json` (or ask Claude to do it).

## Tools
## Tool annotations
Every tool is annotated per the MCP spec (readOnlyHint / destructiveHint /
idempotentHint / openWorldHint) so clients know its blast radius before
calling it. Only `request_callback` is non-read-only (it sends an email).

get_company_info, get_social_links, get_contact_methods, get_rating,
list_services, get_service, list_ai_stack, get_faq, get_faq_audio, get_reviews,
list_brands, get_site_map, search_site, get_full_profile, get_portfolio,
check_slot_availability, request_callback, check_build_status, get_usage_stats.

## Resources
musfiraai://company, musfiraai://services, musfiraai://faq, musfiraai://reviews,
musfiraai://portfolio

## Prompts
draft_client_reply

## Automated quality & release pipeline (GitHub Actions)

- **CI Guard** (`ci-guard.yml`) — runs on every push to `main`: smoke-tests the
  code, waits for Manufact to deploy, then verifies the *live* URL is
  healthy. If either check fails, it automatically reverts the commit and
  pushes the revert — the live server self-heals within a couple of minutes.
- **Auto releases** — every push that passes CI is tagged (`v1.0.0`,
  `v1.0.1`, ...) and published as a GitHub Release with auto-generated notes.
- **Uptime monitor** (`uptime.yml`) — pings `/health` every 15 minutes and
  maintains `uptime/badge.json` (a shields.io endpoint badge) and
  `uptime/log.json` (rolling history).
- **Secret scanning + push protection** — enabled on this repo (GitHub's free
  tier for public repos), plus Dependabot vulnerability alerts.
