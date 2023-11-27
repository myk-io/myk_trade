from piccolo.apps.user.tables import BaseUser
from piccolo.columns import UUID, Date, Float, ForeignKey, Numeric, Varchar
from piccolo.table import Table


class CurrencyModel(Table):
    code = Varchar(length=5)
    name = Varchar(length=200)
    to_base_rate = Float(
        default=1.0,
        help_text="Rate to convert to base currency (USD)",
    )


class WalletModel(Table):
    uuid = UUID(primary_key=True)
    user_id = ForeignKey(BaseUser)
    name = Varchar(length=200)
    currency = ForeignKey(CurrencyModel)
    created_at = Date()
    balance = Numeric(digits=(20, 2))


class TransactionModel(Table):
    sender_wallet_id = ForeignKey(WalletModel)
    receiver_wallet_id = ForeignKey(WalletModel)
    amount = Numeric(digits=(20, 2))
    currency = ForeignKey(CurrencyModel)
    created_at = Date()
    status = Varchar(length=200)
