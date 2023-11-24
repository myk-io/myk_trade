from fastapi import APIRouter
from fastapi.requests import Request
from piccolo.apps.user.tables import BaseUser

from myk_trade.db.models.transactions import WalletModel

router = APIRouter()


@router.get("/")
async def get_profile(
    request: Request,
) -> dict:
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
