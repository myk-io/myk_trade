from piccolo.apps.user.tables import BaseUser
from piccolo.columns import UUID, Date, Float, ForeignKey, Varchar
from piccolo.table import Table


class CurrencyModel(Table):
    code = Varchar(length=5)
    name = Varchar(length=200)


class WalletModel(Table):
    uuid = UUID(primary_key=True)
    user_id = ForeignKey(BaseUser)
    name = Varchar(length=200)
    currency = ForeignKey(CurrencyModel)
    created_at = Date()
    balance = Float()


class TransactionModel(Table):
    sender_wallet_id = ForeignKey(WalletModel)
    receiver_wallet_id = ForeignKey(WalletModel)
    amount = Float()
    currency = ForeignKey(CurrencyModel)
    created_at = Date()
    status = Varchar(length=200)
