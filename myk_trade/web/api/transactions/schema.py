from pydantic import BaseModel


class TransactionsCount(BaseModel):
    """Simple message model."""

    count: int


class TransactionCreate(BaseModel):
    """Simple message model."""

    sender_wallet_uuid: str
    recipient_wallet_uuid: str
    amount: float
