# Musfiraai MCP Server

MCP server exposing Musfiraai's company info, services, AI stack, FAQ, reviews,
brands, and contact details as tools/resources/prompts for any MCP-compatible
AI client.

## Run locally

```
pip install -r requirements.txt
python server.py                 # stdio (Claude Desktop)
MCP_TRANSPORT=streamable-http PORT=8000 python server.py   # HTTP (remote)
```

## Tools
get_company_info, get_social_links, get_contact_methods, get_rating,
list_services, get_service, list_ai_stack, get_faq, get_reviews, list_brands,
get_site_map, search_site, get_full_profile.

## Resources
musfiraai://company, musfiraai://services, musfiraai://faq, musfiraai://reviews

## Prompts
draft_client_reply
