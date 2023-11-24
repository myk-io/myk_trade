from pathlib import Path

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

APP_ROOT = Path(__file__).parent.parent.parent.parent

templates = Jinja2Templates(directory=APP_ROOT / "templates")


@router.get("/profile", response_class=HTMLResponse)
async def send_echo_message(
    request: Request,
) -> HTMLResponse:
    """
    Sends echo back to user.

    :param incoming_message: incoming message.
    :returns: message same as the incoming.
    """

    return templates.TemplateResponse(
        "profile.html",
        {
            "request": {"type": "html"},
            "title": "Myk Trade",
        },
    )
