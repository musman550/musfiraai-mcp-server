import json
import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("musfiraai")

# ---------------------------------------------------------------------------
# Data — loaded from data.json (edit that file directly, e.g. on GitHub, and
# push to main; Manufact auto-redeploys). No code changes needed to update
# company info, services, FAQ, reviews, brands, or the site map.
# ---------------------------------------------------------------------------

_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
with open(_DATA_PATH, encoding="utf-8") as _f:
    _DATA = json.load(_f)

COMPANY = _DATA["company"]
SOCIALS = _DATA["socials"]
RATING = _DATA["rating"]
SERVICES = _DATA["services"]
AI_STACK = _DATA["ai_stack"]
FAQ = _DATA["faq"]
REVIEWS = _DATA["reviews"]
BRANDS = _DATA["brands"]
BREADCRUMBS = _DATA["breadcrumbs"]

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


@mcp.tool()
def request_callback(name: str, need: str, contact: str) -> dict:
    """Submit a lead: someone wants Musfiraai to build them a free automation
    system. Emails the request straight to Musfiraai so a human follows up.
    `name` = the requester's name, `need` = what they want built, `contact` =
    their email or WhatsApp number to reply to."""
    import smtplib
    from email.message import EmailMessage

    sender = os.environ.get("GMAIL_ADDRESS")
    app_password = os.environ.get("GMAIL_APP_PASSWORD")

    if not sender or not app_password:
        return {
            "sent": False,
            "reason": "Email is not configured on this server yet.",
            "fallback": f"Please contact Musfiraai directly — WhatsApp {COMPANY['whatsapp']} or email {COMPANY['email']}.",
        }

    msg = EmailMessage()
    msg["Subject"] = f"New Musfiraai lead: {name}"
    msg["From"] = sender
    msg["To"] = COMPANY["email"]
    msg["Reply-To"] = contact
    msg.set_content(
        f"New lead from the Musfiraai MCP server.\n\n"
        f"Name: {name}\n"
        f"Contact: {contact}\n"
        f"Need: {need}\n"
    )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, app_password)
            server.send_message(msg)
        return {"sent": True, "message": f"Thanks {name} — Musfiraai will follow up at {contact} soon."}
    except Exception as e:
        return {
            "sent": False,
            "reason": str(e),
            "fallback": f"Please contact Musfiraai directly — WhatsApp {COMPANY['whatsapp']} or email {COMPANY['email']}.",
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
