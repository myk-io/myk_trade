from fastapi.routing import APIRouter

from myk_trade.web.ui import ui

ui_router = APIRouter()
ui_router.include_router(ui.router, tags=["ui"])
