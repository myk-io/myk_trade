from fastapi.routing import APIRouter

from myk_trade.web.private_api import profile

api_router = APIRouter()
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])
