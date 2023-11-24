import datetime

from fastapi import APIRouter

from myk_trade.db.models import transactions
from myk_trade.web.api.transactions.schema import *

router = APIRouter()


@router.get("/total")
async def get_trans() -> TransactionsCount:
    """
    Sends echo back to user.

    :param incoming_message: incoming message.
    :returns: message same as the incoming.
    """

    total_transactions = await transactions.TransactionModel.count()

    return TransactionsCount(count=total_transactions)


@router.get("/")
async def get_trans(
    days: int = None,
    currency: str = None,
) -> TransactionsCount:
    """
    Sends echo back to user.

    :param incoming_message: incoming message.
    :returns: message same as the incoming.
    """

    if days is None:
        days = 30

    if currency is None:
        currency = "uah"

    total_transactions = (
        await transactions.TransactionModel.count()
        .where(
            transactions.TransactionModel.created_at
            > datetime.datetime.now() - datetime.timedelta(days=days),
        )
        .where(
            transactions.TransactionModel.currency == currency,
        )
    )
    return TransactionsCount(count=total_transactions)
