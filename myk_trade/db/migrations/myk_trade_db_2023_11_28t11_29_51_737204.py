from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Date, Timestamp
from piccolo.columns.defaults.date import DateNow
from piccolo.columns.defaults.timestamp import TimestampNow

ID = "2023-11-28T11:29:51:737204"
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
        column_name="created_at",
        db_column_name="created_at",
        params={"default": TimestampNow()},
        old_params={"default": DateNow()},
        column_class=Timestamp,
        old_column_class=Date,
    )

    manager.alter_column(
        table_class_name="WalletModel",
        tablename="wallet_model",
        column_name="created_at",
        db_column_name="created_at",
        params={"default": TimestampNow()},
        old_params={"default": DateNow()},
        column_class=Timestamp,
        old_column_class=Date,
    )

    return manager
