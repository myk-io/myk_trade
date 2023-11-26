from fastapi.routing import APIRouter
from piccolo_api.crud.endpoints import PiccoloCRUD

from myk_trade.db.models import transactions as transactions_model
from myk_trade.web.api import docs, echo, monitoring, profile, redis, transactions

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)

api_router.include_router(redis.router, prefix="/redis", tags=["redis"])
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])

api_router.include_router(
    transactions.router,
    prefix="/transactions",
    tags=["transactions"],
)
api_router.include_router(
    PiccoloCRUD(transactions_model.TransactionModel, read_only=True),
    prefix="/transactions",
    tags=["transactions"],
)
