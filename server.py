import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("musfiraai")

# ---------------------------------------------------------------------------
# Data (sourced from musfiraai.com structured data)
# ---------------------------------------------------------------------------

COMPANY = {
    "name": "Musfiraai",
    "alternate_name": "Automate With Musfira AI",
    "founder": "Muhammad Usman",
    "founder_title": "Founder & AI Automation Engineer",
    "area_served": "Worldwide",
    "description": "Free AI automation platform offering all AI agents, custom bots, n8n workflows, call agents and chatbots — ready or on-demand — at zero cost.",
    "email": "musfiraai329@gmail.com",
    "whatsapp": "+923217358096",
    "whatsapp_link": "https://wa.me/923217358096",
    "price_range": "Free",
    "region": "Pakistan",
    "url": "https://musfiraai.com/",
}

SOCIALS = {
    "instagram": "https://instagram.com/musma_n55",
    "youtube": "https://youtube.com/@automatewithmusfiraai",
    "linkedin": "https://www.linkedin.com/in/muhammad-usman-b3218b39b",
    "telegram": "https://t.me/musfiraai",
    "discord": "https://discord.gg/snaBYJzM",
}

RATING = {"value": 4.9, "count": 10, "best": 5}

SERVICES = [
    {"name": "Video Automation", "description": "Playwright-driven clip generation, FFmpeg render pipelines, and auto-upload."},
    {"name": "AI Orchestration", "description": "Musfira AI, Gemini, Claude and Meta AI chained with fallback logic and cross-model dedup."},
    {"name": "Desktop Dashboards", "description": "CustomTkinter control panels for monitoring and triggering every bot."},
    {"name": "Voice Systems", "description": "Multi-tier Edge-TTS pipelines with natural pacing."},
    {"name": "Amazon Automation", "description": "SP-API pipelines for repricing, inventory sync, and listing management."},
    {"name": "Web & SEO Engines", "description": "Custom Blogger XML themes, programmatic SEO, and automated redirects."},
    {"name": "LinkedIn Automation", "description": "OAuth-driven posting bots with dedup and SEO-scored content."},
    {"name": "X / Twitter Bots", "description": "OAuth 2.0 PKCE flows with smart posting fallback and content rotation."},
]

AI_STACK = {
    "core_production": ["Musfira AI (in-house)", "Gemini", "Claude", "Meta AI", "Edge-TTS", "FFmpeg", "Playwright", "n8n", "OpenRouter"],
    "available_on_request": ["GPT-4o", "Perplexity", "Grok", "DeepSeek"],
}

FAQ = [
    {"question": "What is Musfiraai?", "answer": "Musfiraai is a free AI automation platform that builds and delivers AI agents, chatbots, call agents, and n8n workflows at zero cost — operated by Muhammad Usman as an alternative to paid automation agencies on Fiverr and Upwork."},
    {"question": "What does Musfiraai automate?", "answer": "Everything paid AI agencies sell: AI agents, custom bots, n8n/Make workflows, call agents, chatbots, YouTube/Amazon/LinkedIn systems — ready-made or on demand, all free."},
    {"question": "Is this actually free?", "answer": "Yes — ready systems and on-demand custom builds (n8n, bots, call agents, chatbots) are 100% free with lifetime access. No invoice, no retainer, no hidden tier."},
    {"question": "Which AI agents does Musfiraai use?", "answer": "Musfira AI (in-house model) leads the fleet, alongside Gemini, Claude, Meta AI, Edge-TTS, FFmpeg, Playwright, n8n, and OpenRouter as the core production stack, with GPT-4o, Perplexity, Grok, DeepSeek, and more available on request."},
    {"question": "How do I claim a free automation system?", "answer": "Message WhatsApp +92 321 7358096 or email musfiraai329@gmail.com with what you need. We map the stack, build it, and hand it off — free."},
    {"question": "Is Musfiraai automation compliant with platform rules?", "answer": "Yes. Every pipeline includes retry logic, rate-limit handling, and SHA-256 deduplication designed to operate within each platform's terms of service."},
    {"question": "How fast can Musfiraai build a custom system?", "answer": "Timelines depend on scope, but most single-platform systems are delivered within a limited number of free build slots per month — contact via WhatsApp for current availability."},
    {"question": "What happens after the free build slots run out?", "answer": "New claims wait for the next month's slot batch, but anything already handed off stays yours permanently — nothing gets revoked, paused, or paywalled after delivery."},
    {"question": "Do I keep the source code and access after handoff?", "answer": "Yes — every system ships as complete, ready-to-run code files, yours to keep permanently. You connect your own API keys or accounts for any platform the system integrates with. No lock-in, no dependency on Musfiraai staying involved for it to keep running."},
]

REVIEWS = [
    {"author": "Verified Google Review", "rating": 5, "text": "Musfira AI built a custom Python script that automated our video rendering and text-to-speech voiceovers — a 2-hour daily task became a single click."},
    {"author": "Verified Google Review", "rating": 5, "text": "In a market full of copy-paste AI solutions, Musfira AI builds bots tailored to real business problems — their free custom bot proved it instantly."},
    {"author": "Verified Google Review", "rating": 5, "text": "They built a custom auto-responder for our daily FAQs. It feels natural and human — you can tell real care went into it."},
    {"author": "Verified Google Review", "rating": 5, "text": "They understood our requirements without endless meetings, then delivered a Python/Playwright automation that runs flawlessly — completely free of charge."},
]

BRANDS = [
    {"name": "Automate With Musfira AI", "description": "Faceless YouTube Shorts live-streaming automation channel."},
    {"name": "Amazon Seller Automation", "description": "SP-API based repricing and reporting system."},
]

BREADCRUMBS = [
    {"name": "Home", "url": "https://musfiraai.com/#home"},
    {"name": "Portfolio", "url": "https://musfiraai.com/#portfolio"},
    {"name": "Platform", "url": "https://musfiraai.com/#platform"},
    {"name": "Blog", "url": "https://musfiraai.com/#blog"},
]

# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def get_company_info() -> dict:
    """Get Musfiraai company/brand info: founder, description, contact, region, url."""
    return COMPANY


@mcp.tool()
def get_social_links() -> dict:
    """Get Musfiraai's social media links (Instagram, YouTube, LinkedIn, Telegram, Discord)."""
    return SOCIALS


@mcp.tool()
def get_contact_methods() -> dict:
    """Get every way to contact Musfiraai: WhatsApp, email, and socials."""
    return {
        "whatsapp": COMPANY["whatsapp"],
        "whatsapp_link": COMPANY["whatsapp_link"],
        "email": COMPANY["email"],
        "socials": SOCIALS,
    }


@mcp.tool()
def get_rating() -> dict:
    """Get Musfiraai's aggregate customer rating (value, review count, best possible)."""
    return RATING


@mcp.tool()
def list_services() -> list:
    """List all automation services/modules Musfiraai offers."""
    return SERVICES


@mcp.tool()
def get_service(name: str) -> dict:
    """Get one service by name (case-insensitive partial match). Returns an
    error dict if nothing matches."""
    q = name.lower()
    for s in SERVICES:
        if q in s["name"].lower():
            return s
    return {"error": f"No service matching '{name}'", "available": [s["name"] for s in SERVICES]}


@mcp.tool()
def list_ai_stack() -> dict:
    """List the AI models/tools in Musfiraai's production stack and what's
    available on request."""
    return AI_STACK


@mcp.tool()
def get_faq(question: str = "") -> list:
    """Get FAQ entries. If `question` is given, returns entries whose question
    or answer contains that text (case-insensitive substring match); otherwise
    returns all FAQ entries."""
    if not question:
        return FAQ
    q = question.lower()
    return [f for f in FAQ if q in f["question"].lower() or q in f["answer"].lower()]


@mcp.tool()
def get_reviews(min_rating: int = 0) -> list:
    """Get verified customer reviews, optionally filtered by minimum rating (1-5)."""
    return [r for r in REVIEWS if r["rating"] >= min_rating]


@mcp.tool()
def list_brands() -> list:
    """List the automation brands/channels operated under Musfiraai."""
    return BRANDS


@mcp.tool()
def get_site_map() -> list:
    """Get the site's top-level navigation sections (breadcrumbs)."""
    return BREADCRUMBS


@mcp.tool()
def search_site(query: str) -> dict:
    """Search across services, FAQ, reviews, and brands for a keyword and
    return matches grouped by section."""
    q = query.lower()
    return {
        "services": [s for s in SERVICES if q in s["name"].lower() or q in s["description"].lower()],
        "faq": [f for f in FAQ if q in f["question"].lower() or q in f["answer"].lower()],
        "reviews": [r for r in REVIEWS if q in r["text"].lower()],
        "brands": [b for b in BRANDS if q in b["name"].lower() or q in b["description"].lower()],
    }


@mcp.tool()
def get_full_profile() -> dict:
    """Get the complete Musfiraai profile in one call: company, socials, rating,
    services, AI stack, brands, and FAQ. Useful for a single-shot overview."""
    return {
        "company": COMPANY,
        "socials": SOCIALS,
        "rating": RATING,
        "services": SERVICES,
        "ai_stack": AI_STACK,
        "brands": BRANDS,
        "faq": FAQ,
        "reviews": REVIEWS,
    }


# ---------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------


@mcp.resource("musfiraai://company")
def resource_company() -> dict:
    """Musfiraai company info."""
    return COMPANY


@mcp.resource("musfiraai://services")
def resource_services() -> list:
    """Musfiraai service catalog."""
    return SERVICES


@mcp.resource("musfiraai://faq")
def resource_faq() -> list:
    """Musfiraai FAQ list."""
    return FAQ


@mcp.resource("musfiraai://reviews")
def resource_reviews() -> list:
    """Musfiraai customer reviews."""
    return REVIEWS


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------


@mcp.prompt()
def draft_client_reply(client_need: str) -> str:
    """Draft a WhatsApp/email reply to a prospective client describing what
    they need, using Musfiraai's tone and offer."""
    return (
        f"Write a short, friendly reply from Musfiraai (founder: {COMPANY['founder']}) "
        f"to a prospective client who needs: {client_need}. "
        f"Mention it's built free with lifetime access and complete source code handoff. "
        f"Ask them to confirm details on WhatsApp ({COMPANY['whatsapp']}) or email "
        f"({COMPANY['email']}) to start the build."
    )


if __name__ == "__main__":
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    if transport in ("streamable-http", "sse"):
        import uvicorn
        from contextlib import AsyncExitStack

        port = int(os.environ.get("PORT", "8000"))
        mcp.settings.host = "0.0.0.0"
        mcp.settings.port = port

        mcp.streamable_http_app()  # lazily initializes mcp.session_manager

        _static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
        with open(os.path.join(_static_dir, "index.html"), "rb") as f:
            DOCS_HTML = f.read()

        # Raw ASGI app, hand-dispatched by exact path, so both "/mcp" and
        # "/mcp/" work with NO redirect — some cloud health-checkers POST the
        # bare mcpUrl and don't follow a 307 to the trailing-slash route that
        # FastMCP's built-in Starlette app would otherwise require.
        # "/" serves a human-readable docs/landing page; "/mcp" is the API.
        async def app(scope, receive, send):
            if scope["type"] == "lifespan":
                async with AsyncExitStack() as stack:
                    await stack.enter_async_context(mcp.session_manager.run())
                    while True:
                        message = await receive()
                        if message["type"] == "lifespan.startup":
                            await send({"type": "lifespan.startup.complete"})
                        elif message["type"] == "lifespan.shutdown":
                            await send({"type": "lifespan.shutdown.complete"})
                            return
                return
            path = scope["path"]
            if path == "/health":
                await send({"type": "http.response.start", "status": 200,
                             "headers": [(b"content-type", b"text/plain")]})
                await send({"type": "http.response.body", "body": b"ok"})
                return
            if path == "/":
                await send({"type": "http.response.start", "status": 200,
                             "headers": [(b"content-type", b"text/html; charset=utf-8")]})
                await send({"type": "http.response.body", "body": DOCS_HTML})
                return
            if path in ("/mcp", "/mcp/"):
                await mcp.session_manager.handle_request(scope, receive, send)
                return
            await send({"type": "http.response.start", "status": 404,
                         "headers": [(b"content-type", b"text/plain")]})
            await send({"type": "http.response.body", "body": b"Not Found"})

        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        mcp.run()
