from pydantic import BaseModel


class TransactionsCount(BaseModel):
    """Simple message model."""

    count: int
