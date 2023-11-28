import datetime
import logging
from pathlib import Path

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from piccolo.query import Sum

from myk_trade.db.models.transactions import (
    CurrencyModel,
    TransactionModel,
    WalletModel,
)

router = APIRouter()

log = logging.getLogger(__name__)

APP_ROOT = Path(__file__).parent.parent.parent.parent

templates = Jinja2Templates(directory=APP_ROOT / "templates")


@router.get("/")
async def send_echo_message(
    request: Request,
):
    """
    Sends echo back to user.

    :param incoming_message: incoming message.
    :returns: message same as the incoming.
    """

    transactions_sum_select = TransactionModel.select(
        TransactionModel.currency.code,
        TransactionModel.currency.to_base_rate,
        Sum(TransactionModel.amount),
    ).group_by(
        TransactionModel.currency.code,
        TransactionModel.currency.to_base_rate,
    )

    transactions_sum_by_currency = await transactions_sum_select.run()
    transactions_amount = 0
    for t in transactions_sum_by_currency:
        transactions_amount += float(t.get("sum")) * t.get("currency.to_base_rate")

    transactions_sum_by_currency_24h = await transactions_sum_select.where(
        TransactionModel.created_at
        > datetime.datetime.now() - datetime.timedelta(days=1),
    ).run()
    transactions_amount_24h = 0
    for t in transactions_sum_by_currency_24h:
        transactions_amount_24h += float(t.get("sum")) * t.get("currency.to_base_rate")

    currencies = await CurrencyModel.select(
        CurrencyModel.all_columns(),
    ).run()

    return templates.TemplateResponse(
        "home.html",
        {
            "request": {"type": "html"},
            "is_authenticated": request.user.is_authenticated,
            "transactions_amount": transactions_amount,
            "transactions_amount_24h": transactions_amount_24h,
            "currencies": currencies,
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
