from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response
from piccolo.apps.user.tables import BaseUser

from myk_trade.db.models.transactions import WalletModel

router = APIRouter()


@router.get("/")
async def get_profile(
    request: Request,
) -> dict:
    if request.user.is_authenticated is False:
        return Response(status_code=401, content="Unauthorized")

    user = (
        await BaseUser.select(
            exclude_secrets=True,
        )
        .where(
            BaseUser.id == request.user.user.id,
        )
        .first()
        .run()
    )
    return user


@router.get("/wallets")
async def get_wallets(
    request: Request,
) -> list:
    if request.user.is_authenticated is False:
        return Response(status_code=401, content="Unauthorized")

    wallets = (
        await WalletModel.select(
            exclude_secrets=True,
        )
        .where(
            WalletModel.user_id == request.user.user.id,
        )
        .run(nested=True)
    )
    return wallets
