import datetime
from pathlib import Path

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from myk_trade.db.models.transactions import TransactionModel, WalletModel

router = APIRouter()

APP_ROOT = Path(__file__).parent.parent.parent.parent

templates = Jinja2Templates(directory=APP_ROOT / "templates")


@router.get("/", response_class=HTMLResponse)
async def send_echo_message(
    request: Request,
) -> HTMLResponse:
    """
    Sends echo back to user.

    :param incoming_message: incoming message.
    :returns: message same as the incoming.
    """

    transactions_total = await TransactionModel.count().run()
    transactions = (
        await TransactionModel.select(
            TransactionModel.all_columns(),
            TransactionModel.currency.code,
        )
        .where(
            TransactionModel.created_at
            > datetime.datetime.now() - datetime.timedelta(days=1),  # for last 24 hours
        )
        .run(nested=True)
    )

    return templates.TemplateResponse(
        "home.html",
        {
            "request": {"type": "html"},
            "is_authenticated": request.user.is_authenticated,
            "transactions_total": transactions_total,
            "transactions": transactions,
            "user": request.user.user,
            "title": "Myk Trade",
        },
    )


@router.get("/profile", response_class=HTMLResponse)
async def send_echo_message(
    request: Request,
) -> HTMLResponse:
    """
    Sends echo back to user.

    :param incoming_message: incoming message.
    :returns: message same as the incoming.
    """

    if request.user.is_authenticated is False:
        return RedirectResponse(url="/login")
    else:
        wallets = (
            await WalletModel.select(
                WalletModel.all_columns(),
                WalletModel.currency.code,
            )
            .where(
                WalletModel.user_id == request.user.user.id,
            )
            .run(nested=True)
        )

        return templates.TemplateResponse(
            "profile.html",
            {
                "request": {"type": "html"},
                "is_authenticated": request.user.is_authenticated,
                "user": request.user.user,
                "title": "Myk Trade",
                "wallets": wallets,
            },
        )
