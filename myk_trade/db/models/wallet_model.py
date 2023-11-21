from piccolo.apps.user.tables import BaseUser
from piccolo.columns import ForeignKey, Varchar
from piccolo.table import Table


class WalletModel(Table):
    """Model for demo purpose."""

    user_id = ForeignKey(BaseUser)
    name = Varchar(length=200)  # noqa: WPS432
    currency = Varchar(length=200)
    amount = Varchar(length=200)
