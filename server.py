import json
import os
import uuid
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("musfiraai")

# ---------------------------------------------------------------------------
# Build-status tracking — stored as JSON in the PRIVATE guardian repo (not
# this public one), since it holds customer names/contacts. Read/written via
# the GitHub Contents API. GITHUB_TOKEN must have push access to that repo.
# ---------------------------------------------------------------------------
_GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
_STATUS_REPO = os.environ.get("GITHUB_STATUS_REPO", "musman550/musfiraai-mcp-guardian")
_STATUS_PATH = os.environ.get("GITHUB_STATUS_PATH", "data/builds.json")
_STATUS_API = f"https://api.github.com/repos/{_STATUS_REPO}/contents/{_STATUS_PATH}"

# ---------------------------------------------------------------------------
# Data — loaded from data.json (edit that file directly, e.g. on GitHub, and
# push to main; Manufact auto-redeploys). No code changes needed to update
# company info, services, FAQ, reviews, brands, portfolio, or availability.
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
PORTFOLIO = _DATA["portfolio"]
AVAILABILITY = _DATA["availability"]

# ---------------------------------------------------------------------------
# Lightweight in-memory usage tracking (resets on restart — see
# get_usage_stats for details). Every @tracked tool call increments a
# per-tool counter and updates the "since" timestamp.
# ---------------------------------------------------------------------------

import functools
import time

_USAGE = {"since": time.time(), "calls": {}}


def tracked(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        _USAGE["calls"][fn.__name__] = _USAGE["calls"].get(fn.__name__, 0) + 1
        return fn(*args, **kwargs)
    return wrapper


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
@tracked
def get_company_info() -> dict:
    """Get Musfiraai company/brand info: founder, description, contact, region, url."""
    return COMPANY


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
@tracked
def get_social_links() -> dict:
    """Get Musfiraai's social media links (Instagram, YouTube, LinkedIn, Telegram, Discord)."""
    return SOCIALS


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
@tracked
def get_contact_methods() -> dict:
    """Get every way to contact Musfiraai: WhatsApp, email, and socials."""
    return {
        "whatsapp": COMPANY["whatsapp"],
        "whatsapp_link": COMPANY["whatsapp_link"],
        "email": COMPANY["email"],
        "socials": SOCIALS,
    }


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
@tracked
def get_rating() -> dict:
    """Get Musfiraai's aggregate customer rating (value, review count, best possible)."""
    return RATING


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
@tracked
def list_services() -> list:
    """List all automation services/modules Musfiraai offers."""
    return SERVICES


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
@tracked
def get_service(name: str) -> dict:
    """Get one service by name (case-insensitive partial match). Returns an
    error dict if nothing matches."""
    q = name.lower()
    for s in SERVICES:
        if q in s["name"].lower():
            return s
    return {"error": f"No service matching '{name}'", "available": [s["name"] for s in SERVICES]}


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
@tracked
def list_ai_stack() -> dict:
    """List the AI models/tools in Musfiraai's production stack and what's
    available on request."""
    return AI_STACK


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
@tracked
def get_faq(question: str = "") -> list:
    """Get FAQ entries. If `question` is given, returns entries whose question
    or answer contains that text (case-insensitive substring match); otherwise
    returns all FAQ entries."""
    if not question:
        return FAQ
    q = question.lower()
    return [f for f in FAQ if q in f["question"].lower() or q in f["answer"].lower()]


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
@tracked
def get_reviews(min_rating: int = 0) -> list:
    """Get verified customer reviews, optionally filtered by minimum rating (1-5)."""
    return [r for r in REVIEWS if r["rating"] >= min_rating]


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
@tracked
def list_brands() -> list:
    """List the automation brands/channels operated under Musfiraai."""
    return BRANDS


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
@tracked
def get_site_map() -> list:
    """Get the site's top-level navigation sections (breadcrumbs)."""
    return BREADCRUMBS


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
@tracked
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


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
@tracked
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


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
@tracked
def get_portfolio() -> dict:
    """Get Muhammad Usman's freelance portfolio: SEO/GEO/AEO background,
    experience stats, and the skill categories behind Musfiraai's automation
    work (video/voice, AI orchestration, dashboards, Amazon, web/SEO, LinkedIn)."""
    return PORTFOLIO


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
@tracked
def check_slot_availability() -> dict:
    """Check how many free monthly automation-build slots are left. This
    number is set manually in data.json (there's no live booking system
    behind it) so it reflects whatever Musfiraai last updated."""
    limit = AVAILABILITY.get("monthly_slot_limit", 0)
    used = AVAILABILITY.get("slots_used_this_month", 0)
    remaining = max(limit - used, 0)
    return {
        "month": AVAILABILITY.get("month"),
        "monthly_slot_limit": limit,
        "slots_used_this_month": used,
        "slots_remaining": remaining,
        "last_updated": AVAILABILITY.get("last_updated"),
        "note": "Manually maintained — contact Musfiraai to confirm real-time availability." if remaining <= 0 else None,
    }


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=False, openWorldHint=True))
@tracked
def request_callback(name: str, need: str, contact: str) -> dict:
    """Submit a lead: someone wants Musfiraai to build them a free automation
    system. Emails the request straight to Musfiraai so a human follows up,
    and creates a trackable request ID (see check_build_status).
    `name` = the requester's name, `need` = what they want built, `contact` =
    their email or WhatsApp number to reply to."""
    import smtplib
    from email.message import EmailMessage

    request_id = _create_build_record(name, need, contact)

    sender = os.environ.get("GMAIL_ADDRESS")
    app_password = os.environ.get("GMAIL_APP_PASSWORD")

    if not sender or not app_password:
        return {
            "sent": False,
            "request_id": request_id,
            "reason": "Email is not configured on this server yet.",
            "fallback": f"Please contact Musfiraai directly — WhatsApp {COMPANY['whatsapp']} or email {COMPANY['email']}.",
        }

    msg = EmailMessage()
    msg["Subject"] = f"New Musfiraai lead: {name} [{request_id or 'no-id'}]"
    msg["From"] = sender
    msg["To"] = COMPANY["email"]
    msg["Reply-To"] = contact
    msg.set_content(
        f"New lead from the Musfiraai MCP server.\n\n"
        f"Request ID: {request_id or '(status tracking unavailable)'}\n"
        f"Name: {name}\n"
        f"Contact: {contact}\n"
        f"Need: {need}\n"
    )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, app_password)
            server.send_message(msg)
        reply = {"sent": True, "message": f"Thanks {name} — Musfiraai will follow up at {contact} soon."}
        if request_id:
            reply["request_id"] = request_id
            reply["track_status_with"] = f"check_build_status('{request_id}')"
        return reply
    except Exception as e:
        return {
            "sent": False,
            "request_id": request_id,
            "reason": str(e),
            "fallback": f"Please contact Musfiraai directly — WhatsApp {COMPANY['whatsapp']} or email {COMPANY['email']}.",
        }


def _github_headers():
    return {
        "Authorization": f"token {_GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "musfiraai-mcp-server",
    }


def _create_build_record(name: str, need: str, contact: str):
    """Append a new request to the private status store. Returns the new
    request_id, or None if tracking isn't configured / the write failed
    (request_callback still works without it — email is the source of truth)."""
    if not _GITHUB_TOKEN:
        return None

    import base64
    import datetime
    import random
    import urllib.error
    import urllib.request

    for attempt in range(3):
        try:
            req = urllib.request.Request(_STATUS_API, headers=_github_headers())
            with urllib.request.urlopen(req, timeout=10) as r:
                current = json.loads(r.read().decode())
            sha = current["sha"]
            store = json.loads(base64.b64decode(current["content"]).decode())
        except urllib.error.URLError:
            return None
        except Exception:
            return None

        request_id = f"MFA-{random.randint(1000, 9999)}"
        existing_ids = {r["id"] for r in store.get("requests", [])}
        if request_id in existing_ids:
            continue  # extremely unlikely collision, just retry with a new random id

        store.setdefault("requests", []).append({
            "id": request_id,
            "name": name,
            "contact": contact,
            "need": need,
            "status": "Received",
            "created_utc": datetime.datetime.utcnow().isoformat() + "Z",
            "updated_utc": datetime.datetime.utcnow().isoformat() + "Z",
        })

        payload = {
            "message": f"New build request {request_id}",
            "content": base64.b64encode(json.dumps(store, indent=2).encode()).decode(),
            "sha": sha,
        }
        try:
            put_req = urllib.request.Request(
                _STATUS_API, method="PUT", headers=_github_headers(),
                data=json.dumps(payload).encode(),
            )
            with urllib.request.urlopen(put_req, timeout=10):
                return request_id
        except urllib.error.HTTPError as e:
            if e.code == 409:
                continue  # someone else wrote in between — retry with fresh sha
            return None
        except Exception:
            return None

    return None


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
@tracked
def check_build_status(request_id: str) -> dict:
    """Check the status of a free-build request by its request ID (e.g.
    "MFA-4821", returned when the request was submitted via
    request_callback). Status is one of: Received, Queued, Building,
    Delivered."""
    if not _GITHUB_TOKEN:
        return {"error": "Status tracking isn't configured on this server."}

    import base64
    import urllib.error
    import urllib.request

    try:
        req = urllib.request.Request(_STATUS_API, headers=_github_headers())
        with urllib.request.urlopen(req, timeout=10) as r:
            current = json.loads(r.read().decode())
        store = json.loads(base64.b64decode(current["content"]).decode())
    except Exception as e:
        return {"error": f"Could not check status right now: {e}"}

    for r in store.get("requests", []):
        if r["id"].lower() == request_id.strip().lower():
            return {
                "id": r["id"],
                "status": r["status"],
                "submitted": r.get("created_utc"),
                "last_updated": r.get("updated_utc"),
            }
    return {"error": f"No request found with ID '{request_id}'. Double-check the ID you were given."}


# Voices: pick by language. Matches Usman's existing edge-tts stack.
_VOICES = {
    "en": "en-US-AriaNeural",
    "hi": "hi-IN-MadhurNeural",
    "ur": "ur-PK-AsadNeural",
}
_AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "audio")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True, openWorldHint=False))
@tracked
def get_faq_audio(question: str, language: str = "en") -> dict:
    """Answer a FAQ question as spoken audio (text-to-speech via edge-tts).
    `language` is one of "en" (English), "hi" (Hindi), or "ur" (Urdu) and
    picks the voice; the FAQ text itself is only stored in English. Returns
    a URL to an MP3 the caller can play or link to. Audio files are
    generated on demand and are not guaranteed to persist across restarts."""
    matches = get_faq.__wrapped__(question)
    if not matches:
        return {"error": f"No FAQ entry matches '{question}'.", "available_questions": [f["question"] for f in FAQ]}

    answer = matches[0]["answer"]
    voice = _VOICES.get(language, _VOICES["en"])

    try:
        import asyncio
        import edge_tts

        os.makedirs(_AUDIO_DIR, exist_ok=True)
        filename = f"{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(_AUDIO_DIR, filename)

        async def synth():
            communicate = edge_tts.Communicate(answer, voice)
            await communicate.save(filepath)

        asyncio.run(synth())

        base_url = os.environ.get("PUBLIC_BASE_URL", "").rstrip("/")
        audio_url = f"{base_url}/audio/{filename}" if base_url else f"/audio/{filename}"
        return {"question": matches[0]["question"], "answer_text": answer, "audio_url": audio_url, "voice": voice}
    except Exception as e:
        return {"question": matches[0]["question"], "answer_text": answer, "audio_url": None, "error": f"TTS generation failed: {e}"}


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
@tracked
def get_usage_stats() -> dict:
    """See which tools have been called most on this running server instance.
    Counts are in-memory only — they reset whenever the server restarts or
    redeploys, so this reflects recent activity, not all-time history."""
    calls = _USAGE["calls"]
    total = sum(calls.values())
    top = sorted(calls.items(), key=lambda kv: kv[1], reverse=True)
    return {
        "tracking_since": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(_USAGE["since"])),
        "total_calls": total,
        "calls_by_tool": dict(top),
        "note": "In-memory only — resets on restart/redeploy, not a historical log.",
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


@mcp.resource("musfiraai://portfolio")
def resource_portfolio() -> dict:
    """Muhammad Usman's freelance SEO/GEO/AEO + automation portfolio."""
    return PORTFOLIO


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
            if path.startswith("/audio/"):
                fname = path[len("/audio/"):]
                if "/" in fname or ".." in fname:
                    await send({"type": "http.response.start", "status": 400,
                                 "headers": [(b"content-type", b"text/plain")]})
                    await send({"type": "http.response.body", "body": b"Bad Request"})
                    return
                fpath = os.path.join(_AUDIO_DIR, fname)
                if os.path.isfile(fpath):
                    with open(fpath, "rb") as af:
                        body = af.read()
                    await send({"type": "http.response.start", "status": 200,
                                 "headers": [(b"content-type", b"audio/mpeg")]})
                    await send({"type": "http.response.body", "body": body})
                else:
                    await send({"type": "http.response.start", "status": 404,
                                 "headers": [(b"content-type", b"text/plain")]})
                    await send({"type": "http.response.body", "body": b"Not Found"})
                return
            if path == "/build-status":
                query = (scope.get("query_string") or b"").decode()
                params = dict(p.split("=", 1) for p in query.split("&") if "=" in p)
                import urllib.parse
                rid = urllib.parse.unquote(params.get("id", "")).strip()
                if not rid:
                    body = json.dumps({"error": "Missing ?id= query parameter."}).encode()
                    await send({"type": "http.response.start", "status": 400,
                                 "headers": [(b"content-type", b"application/json"),
                                             (b"access-control-allow-origin", b"*")]})
                    await send({"type": "http.response.body", "body": body})
                    return
                result = check_build_status.__wrapped__(rid)
                status_code = 404 if "error" in result else 200
                body = json.dumps(result).encode()
                await send({"type": "http.response.start", "status": status_code,
                             "headers": [(b"content-type", b"application/json"),
                                         (b"access-control-allow-origin", b"*")]})
                await send({"type": "http.response.body", "body": body})
                return
            await send({"type": "http.response.start", "status": 404,
                         "headers": [(b"content-type", b"text/plain")]})
            await send({"type": "http.response.body", "body": b"Not Found"})

        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        mcp.run()
