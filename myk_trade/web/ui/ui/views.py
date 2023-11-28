import datetime
from pathlib import Path

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from myk_trade.db.models.transactions import (
    CurrencyModel,
    TransactionModel,
    WalletModel,
)

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

    transactions_count_24h = (
        await TransactionModel.count()
        .where(
            TransactionModel.created_at
            > datetime.datetime.now() - datetime.timedelta(days=1),  # for last 24 hours
        )
        .run()
    )
    transactions_count = await TransactionModel.count().run()

    transactions_amount_24h = 0
    transactions_amount = 0
    for currency in await CurrencyModel.select(CurrencyModel.all_columns()).run():
        transactions_24h = (
            await TransactionModel.select(
                TransactionModel.all_columns(),
            )
            .where(
                TransactionModel.created_at
                > datetime.datetime.now()
                - datetime.timedelta(days=1),  # for last 24 hours
            )
            .where(
                TransactionModel.currency == currency["id"],
            )
            .run()
        )

        for t in transactions_24h:
            transactions_amount_24h += float(t["amount"]) * float(
                currency["to_base_rate"],
            )

        transactions = (
            await TransactionModel.select(
                TransactionModel.all_columns(),
            )
            .where(
                TransactionModel.currency == currency["id"],
            )
            .run()
        )

        for t in transactions:
            transactions_amount += float(t["amount"]) * float(currency["to_base_rate"])

    transactions = (
        await TransactionModel.select(
            TransactionModel.all_columns(),
            TransactionModel.currency.code,
        )
        .order_by(TransactionModel.id, ascending=False)
        .limit(30)
        .run(nested=True)
    )

    currencies = await CurrencyModel.select(CurrencyModel.all_columns()).run()

    return templates.TemplateResponse(
        "home.html",
        {
            "request": {"type": "html"},
            "is_authenticated": request.user.is_authenticated,
            "transactions_count": transactions_count,
            "transactions_count_24h": transactions_count_24h,
            "transactions_amount": transactions_amount,
            "transactions_amount_24h": transactions_amount_24h,
            "transactions": transactions,
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
