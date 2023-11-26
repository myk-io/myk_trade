from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Float, Varchar

ID = "2023-11-24T23:56:12:868394"
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
        params={"default": 0.0},
        old_params={"default": ""},
        column_class=Float,
        old_column_class=Varchar,
    )

    manager.alter_column(
        table_class_name="WalletModel",
        tablename="wallet_model",
        column_name="amount",
        db_column_name="amount",
        params={"default": 0.0},
        old_params={"default": ""},
        column_class=Float,
        old_column_class=Varchar,
    )

    return manager
