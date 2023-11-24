from piccolo.apps.user.tables import BaseUser
from piccolo.columns import Date, ForeignKey, Varchar
from piccolo.table import Table


class WalletModel(Table):
    """Model for demo purpose."""

    user_id = ForeignKey(BaseUser)
    name = Varchar(length=200)  # noqa: WPS432
    currency = Varchar(length=200)
    amount = Varchar(length=200)


class TransactionModel(Table):
    sender_wallet_id = ForeignKey(WalletModel)
    receiver_wallet_id = ForeignKey(WalletModel)
    amount = Varchar(length=200)
    currency = Varchar(length=200)
    created_at = Date()
    status = Varchar(length=200)
