import datetime
import decimal

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response

from myk_trade.db.models import transactions
from myk_trade.web.api.transactions.schema import TransactionCreate, TransactionsCount

router = APIRouter()


@router.get("/count")
async def get_trans(
    days: int = None,
    currency: str = None,
) -> JSONResponse:
    """
    Sends echo back to user.

    :param incoming_message: incoming message.
    :returns: message same as the incoming.
    """

    if days is None:
        days = 30

    if currency is None:
        total_transactions = (
            await transactions.TransactionModel.count()
            .where(
                transactions.TransactionModel.created_at
                > datetime.datetime.now() - datetime.timedelta(days=days),
            )
            .run()
        )
    else:
        сurrency_code = (
            await transactions.CurrencyModel.select()
            .where(
                transactions.CurrencyModel.code == currency,
            )
            .first()
            .run()
        )

        if сurrency_code is None:
            return Response(status_code=404, content="Currency not found")

        total_transactions = (
            await transactions.TransactionModel.count()
            .where(
                transactions.TransactionModel.created_at
                > datetime.datetime.now() - datetime.timedelta(days=days),
            )
            .where(
                transactions.TransactionModel.currency == сurrency_code.get("id"),
            )
            .run()
        )

    return TransactionsCount(count=total_transactions)


@router.post("/create")
async def create_trans(
    request: Request,
    transaction: TransactionCreate,
) -> JSONResponse:

    if request.user.is_authenticated is False:
        return Response(status_code=401, content="Unauthorized")

    user = request.user.user

    if transaction.sender_wallet_uuid == transaction.recipient_wallet_uuid:
        return Response(
            status_code=400,
            content="Sender and recipient wallets must be different",
        )

    sender_wallet = (
        await transactions.WalletModel.select(
            transactions.WalletModel.all_columns(),
        )
        .where(
            transactions.WalletModel.uuid == transaction.sender_wallet_uuid,
        )
        .first()
        .run()
    )

    if sender_wallet is None:
        return Response(status_code=404, content="Sender wallet not found")

    recipient_wallet = (
        await transactions.WalletModel.select(
            transactions.WalletModel.all_columns(),
        )
        .where(
            transactions.WalletModel.uuid == transaction.recipient_wallet_uuid,
        )
        .first()
        .run()
    )

    if recipient_wallet is None:
        return Response(status_code=404, content="Recipient wallet not found")

    if sender_wallet.get("user_id") != user.id:
        return Response(status_code=403, content="Forbidden")

    if recipient_wallet.get("currency") != sender_wallet.get("currency"):
        return Response(
            status_code=400,
            content="Sender and recipient wallets must be the same currency",
        )

    if sender_wallet.get("balance") < transaction.amount:
        return Response(status_code=403, content="Not enough money")

    if transaction.amount <= 0:
        return Response(status_code=400, content="Invalid amount")

    try:
        transaction.amount = decimal.Decimal(transaction.amount)
    except decimal.InvalidOperation:
        return Response(status_code=400, content="Invalid amount")

    DB = transactions.TransactionModel._meta.db

    async with DB.transaction():
        sender_wallet_balance = sender_wallet.get("balance") - transaction.amount
        recipient_wallet_balance = recipient_wallet.get("balance") + transaction.amount

        await transactions.WalletModel.update(
            {
                "balance": sender_wallet_balance,
            },
        ).where(
            transactions.WalletModel.uuid == transaction.sender_wallet_uuid,
        ).run()

        await transactions.WalletModel.update(
            {
                "balance": recipient_wallet_balance,
            },
        ).where(
            transactions.WalletModel.uuid == transaction.recipient_wallet_uuid,
        ).run()

        await transactions.TransactionModel(
            sender_wallet_id=transaction.sender_wallet_uuid,
            receiver_wallet_id=transaction.recipient_wallet_uuid,
            amount=transaction.amount,
            currency=sender_wallet.get("currency"),
            created_at=datetime.datetime.now(),
            status="success",
        ).save().run()

    return Response(status_code=200, content="Transaction created")
