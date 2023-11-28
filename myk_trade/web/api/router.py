from fastapi.routing import APIRouter
from piccolo_api.crud.endpoints import PiccoloCRUD
from piccolo_api.fastapi.endpoints import FastAPIKwargs, FastAPIWrapper

from myk_trade.db.models import transactions as transactions_model
from myk_trade.web.api import docs, monitoring, profile, transactions

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)

api_router.include_router(profile.router, prefix="/profile", tags=["profile"])

api_router.include_router(
    transactions.router,
    prefix="/transactions",
    tags=["transactions"],
)

crud_wraped = FastAPIWrapper(
    root_url="/transactions",
    fastapi_app=api_router,
    piccolo_crud=PiccoloCRUD(
        transactions_model.TransactionModel,
        max_joins=1,
        read_only=True,
    ),
    fastapi_kwargs=FastAPIKwargs(
        all_routes={"tags": ["transactions"]},
    ),
)
