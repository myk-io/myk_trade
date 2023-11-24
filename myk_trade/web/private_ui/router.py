from fastapi.routing import APIRouter

from myk_trade.web.private_ui import private_ui

ui_router = APIRouter()
ui_router.include_router(private_ui.router, tags=["ui"])
