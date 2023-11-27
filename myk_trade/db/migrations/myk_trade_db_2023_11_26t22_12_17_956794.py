import decimal

from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Float, Numeric

ID = "2023-11-26T22:12:17:956794"
VERSION = "0.117.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID,
        app_name="myk_trade_db",
        description=DESCRIPTION,
    )

    manager.alter_column(
        table_class_name="TransactionModel",
        tablename="transaction_model",
        column_name="amount",
        db_column_name="amount",
        params={"default": decimal.Decimal("0"), "digits": (20, 2)},
        old_params={"default": 0.0, "digits": None},
        column_class=Numeric,
        old_column_class=Float,
    )

    manager.alter_column(
        table_class_name="WalletModel",
        tablename="wallet_model",
        column_name="balance",
        db_column_name="balance",
        params={"default": decimal.Decimal("0"), "digits": (20, 2)},
        old_params={"default": 0.0, "digits": None},
        column_class=Numeric,
        old_column_class=Float,
    )

    return manager
