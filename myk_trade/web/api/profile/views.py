from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response
from piccolo.apps.user.tables import BaseUser
from piccolo_api.token_auth.tables import TokenAuth

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


@router.get("/token")
async def get_token(
    request: Request,
) -> dict:
    if request.user.is_authenticated is False:
        return Response(status_code=401, content="Unauthorized")

    token = (
        await TokenAuth.select(
            TokenAuth.token,
            exclude_secrets=True,
        )
        .where(
            TokenAuth.user == request.user.user,
        )
        .first()
        .run()
    )
    return token  # {"token": token}


@router.post("/token")
async def create_token(
    request: Request,
) -> dict:
    if request.user.is_authenticated is False:
        return Response(status_code=401, content="Unauthorized")

    await TokenAuth.delete().where(
        TokenAuth.user == request.user.user,
    ).run()

    token = await TokenAuth.create_token(request.user.user.id)

    return {"token": token}
